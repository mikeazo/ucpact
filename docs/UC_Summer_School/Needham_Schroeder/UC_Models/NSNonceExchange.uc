(* An EasyUC model of the Needham-Schroeder protocol, as described in Ross
 * Anderson and Roger Needham, "Programming Satan's Computer."
 *
 * This version assumes the exchange of nonces is significant (done in the
 * ideal). The only way I can make the real functionality work is to have
 * all three messages exposed in the direct interface of each party.
 *)

uc_requires Forwarding.
ec_requires +NeedhamSchroeder +PKE +PKE_EPDP +NeedhamSchroederKeys.

direct Pt1Dir {
  (* Request to B *)
  in pt1@ns_req (pt2 : port)

  (* Acceptance from B, with nonces *)
  out ns_acc (n_A : int, n_B : int)@pt1

  (* Acknowledgement to B *)
  in pt1@ns_ack
}

direct Pt2Dir {
  (* Request from A *)
  out ns_req (pt1 : port)@pt2

  (* Acceptance from B *)
  in pt2@ns_acc

  (* Acknowledgement from pt1 *)
  out ns_ack (n_A : int, n_B : int)@pt2
}

direct NSNEDir {
  Pt1D : Pt1Dir
  Pt2D : Pt2Dir
}

functionality NSNEReal implements NSNEDir {
  subfun Fwd1 = Forwarding.Forw
  subfun Fwd2 = Forwarding.Forw
  subfun Fwd3 = Forwarding.Forw

  party Pt1 serves NSNEDir.Pt1D {

    initial state WaitRequest {
      var n_A: int;

      match message with
      | pt1@NSNEDir.Pt1D.ns_req (pt2) => {
          if (envport pt2) {
            n_A <$ dnonce;
            send Fwd1.D.fw_req
                   (intport Pt2,
                    epdp_port_port_cipher_univ.`enc
                      (pt1, pt2,
                       (enc pk_b (epdp_int_port_plain.`enc (n_A, pt1)))))
            and transition WaitFwd2 (pt1, pt2, n_A).
          } else {
            fail.
          }
        }

      | * => { fail. }
      end
    }

    state WaitFwd2 (id_A : port, id_B : port, n_A : int) {
      var n_A' : int;
      var n_B : int;
      var plaintext : ptxt_t;

      match message with
      | Fwd2.D.fw_rsp (_, u) => {
          match epdp_cipher_univ.`dec u with
          | Some ciphertext => {
              plaintext <- dec sk_a ciphertext;
              match epdp_int_int_plain.`dec plaintext with
              | Some nn => {
                  (n_A', n_B) <- nn;
                  if (n_A' <> n_A) {
                    fail.
                  } else {
                    send NSNEDir.Pt1D.ns_acc (n_A, n_B)@id_A
                    and transition WaitAck (id_A, id_B, n_B).
                  }
                }
              | None => { fail. }
              end
            }
          | None => { fail. }
          end
        }

      | * => { fail. }
      end
    }

    state WaitAck (id_A : port, id_B : port, n_B : int) {
      match message with
      | pt1@NSNEDir.Pt1D.ns_ack => {
          if (pt1 <> id_A) { fail. }
          else {
            send Fwd3.D.fw_req
              (intport Pt2,
               epdp_cipher_univ.`enc
                 (enc pk_b (epdp_int_plain.`enc n_B)))
            and transition Final.
          }
        }

      | * => { fail. }
      end
    }

    state Final {
      match message with
      | * => { fail. }
      end
    }
  }

  party Pt2 serves NSNEDir.Pt2D {
    initial state WaitFwd1 {
      var n_A : int;
      var id_A : port;
      var id_B : port;
      var ciphertext : ctxt_t;
      var plaintext : ptxt_t;

      match message with
      | Fwd1.D.fw_rsp (_, u) => {
          match epdp_port_port_cipher_univ.`dec u with
          | Some msg => {
              (id_A, id_B, ciphertext) <- msg;
              plaintext <- dec sk_b ciphertext;
              match epdp_int_port_plain.`dec plaintext with
              | Some ni => {
                  (n_A, id_A) <- ni;
                  send NSNEDir.Pt2D.ns_req (id_A)@id_B
                  and transition WaitAccept (id_A, id_B, n_A).
                }
              | None => { fail. }
              end
            }
          | None => { fail. }
          end
        }

      | * => { fail. }
      end
    }

    state WaitAccept (id_A : port, id_B : port, n_A : int) {
      var n_B : int;

      match message with
      | pt2@NSNEDir.Pt2D.ns_acc => {
          if (pt2 <> id_B) {
            fail.
          } else {
            n_B <$ dnonce;
            send Fwd2.D.fw_req
              (intport Pt1,
               epdp_cipher_univ.`enc
                 (enc pk_a (epdp_int_int_plain.`enc (n_A, n_B))))
            and transition WaitFwd3 (id_A, id_B, n_A, n_B).
          }
        }

      | * => { fail. }
      end
    }

    state WaitFwd3 (id_A : port, id_B : port, n_A : int, n_B : int) {
      var id_B' : port;
      var plaintext : ptxt_t;

      match message with
      | Fwd3.D.fw_rsp (_, u) => {
          match epdp_cipher_univ.`dec u with
          | Some ciphertext => {
              plaintext <- dec sk_b ciphertext;
              match epdp_int_plain.`dec plaintext with
              | Some n_B' => {
                  if (n_B' <> n_B) {
                    fail.
                  } else {
                    send NSNEDir.Pt2D.ns_ack (n_A, n_B)@id_B
                    and transition Final.
                  }
                }
              | None => { fail. }
              end
            }
          | None => { fail. }
          end
        }

      | * => { fail. }
      end
    }

    state Final {
      match message with
      | * => { fail. }
      end
    }
  }
}

adversarial NSNEI2S {
  out leak (pt1 : port, pt2 : port)
  in  ok
}

functionality NSNEIdeal implements NSNEDir NSNEI2S {
  initial state WaitRequest {
    var n_A : int;
    var n_B : int;

    match message with
    | pt1@NSNEDir.Pt1D.ns_req (pt2) => {
        n_A <$ dnonce;
        n_B <$ dnonce;
        send NSNEI2S.leak (pt1, pt2)
        and transition WaitSim1 (pt1, pt2, n_A, n_B).
      }

    | * => { fail. }
    end
  }

  state WaitSim1 (id_A : port, id_B : port, n_A : int, n_B : int) {
    match message with
    | NSNEI2S.ok => {
        send NSNEDir.Pt2D.ns_req (id_A)@id_B
        and transition WaitAccept (id_A, id_B, n_A, n_B).
      }

    | * => { fail. }
    end
  }

  state WaitAccept (id_A : port, id_B : port, n_A : int, n_B : int) {
    match message with
    | pt2@NSNEDir.Pt2D.ns_acc => {
        if (pt2 = id_B) {
          send NSNEI2S.leak (id_A, id_B)
          and transition WaitSim2 (id_A, id_B, n_A, n_B).
        } else {
          fail.
        }
      }

    | * => { fail. }
    end
  }

  state WaitSim2 (id_A : port, id_B : port, n_A : int, n_B : int) {
    match message with
    | NSNEI2S.ok => {
        send NSNEDir.Pt1D.ns_acc (n_A, n_B)@id_A
        and transition WaitAcknowledge (id_A, id_B, n_A, n_B).
      }

    | * => { fail. }
    end
  }

  state WaitAcknowledge (id_A : port, id_B : port, n_A : int, n_B : int) {
    match message with
    | pt1@NSNEDir.Pt1D.ns_ack => {
        if (pt1 = id_A) {
          send NSNEI2S.leak (id_A, id_B)
          and transition WaitSim3 (id_A, id_B, n_A, n_B).
        } else {
          fail.
        }
      }

    | * => { fail. }
    end
  }

  state WaitSim3 (id_A : port, id_B : port, n_A : int, n_B : int) {
    match message with
    | NSNEI2S.ok => {
        send NSNEDir.Pt2D.ns_ack (n_A, n_B)@id_B
        and transition Final.
      }

    | * => { fail. }
    end
  }

  state Final {
    match message with
    | * => { fail. }
    end
  }
}

simulator NSNESim uses NSNEI2S simulates NSNEReal {
  initial state WaitLeak1 {
    var n_A : int;

    match message with
    | NSNEI2S.leak (pt1, pt2) => {
        n_A <$ dnonce;
        send NSNEReal.Fwd1.FwAdv.fw_obs
               (intport NSNEReal.Pt1,
                intport NSNEReal.Pt2,
                epdp_port_port_cipher_univ.`enc
                  (pt1, pt2, (enc pk_b (epdp_int_port_plain.`enc (n_A, pt1)))))
        and transition WaitAdv1 (pt1, pt2, n_A).
      }
    end
  }

  state WaitAdv1 (id_A : port, id_B : port, n_A : int) {
    var id_A' : port;
    var id_B' : port;
    var ciphertext : ctxt_t;

    match message with
    | NSNEReal.Fwd1.FwAdv.fw_ok (pt, u) => {
        if (pt = intport NSNEReal.Pt2) {
          match epdp_port_port_cipher_univ.`dec u with
          | Some msg => {
              (id_A', id_B', ciphertext) <- msg;
              if (id_A' <> id_A \/ id_B' <> id_B) {
                fail.
              } else {
                (* TODO Can the simulator use [sk_b] to check [n_A]?
                 * plaintext <- dec sk_b ciphertext; *)
                send NSNEI2S.ok
                and transition WaitLeak2 (n_A).
              }
            }
          | None => { fail. }
          end
        } else {
          fail.
        }
      }

    | * => { fail. }
    end
  }

  state WaitLeak2 (n_A : int) {
    var n_B : int;

    match message with
    | NSNEI2S.leak (_, _) => {
        n_B <$ dnonce;
        send NSNEReal.Fwd2.FwAdv.fw_obs
               (intport NSNEReal.Pt2,
                intport NSNEReal.Pt1,
                epdp_cipher_univ.`enc
                  (enc pk_a (epdp_int_int_plain.`enc (n_A, n_B))))
        and transition WaitAdv2 (n_B).
      }

    | * => { fail. }
    end
  }

  state WaitAdv2 (n_B : int) {
    match message with
    | NSNEReal.Fwd2.FwAdv.fw_ok (pt, u) => {
        if (pt = intport NSNEReal.Pt1) {
          send NSNEI2S.ok
          and transition WaitLeak3 (n_B).
        } else {
          fail.
        }
      }

    | * => { fail. }

    end
  }

  state WaitLeak3 (n_B : int) {
    match message with
    | NSNEI2S.leak (_, _) => {
        send NSNEReal.Fwd3.FwAdv.fw_obs
               (intport NSNEReal.Pt1,
                intport NSNEReal.Pt2,
                epdp_cipher_univ.`enc
                  (enc pk_b (epdp_int_plain.`enc (n_B))))
        and transition WaitAdv3.
      }

    | * => { fail. }
    end
  }

  state WaitAdv3 {
    match message with
    | NSNEReal.Fwd3.FwAdv.fw_ok (pt, u') => {
        if (pt = intport NSNEReal.Pt2) {
          send NSNEI2S.ok
          and transition Final.
        } else {
          fail.
        }
      }

    | * => { fail. }
    end
  }

  state Final {
    match message with
    | * => { fail. }
    end
  }
}

