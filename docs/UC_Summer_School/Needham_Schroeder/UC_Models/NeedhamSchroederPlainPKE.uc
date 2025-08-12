(* An EasyUC model of the Needham-Schroeder protocol, as described in Ross
 * Anderson and Roger Needham, "Programming Satan's Computer," Section 3.2.
 * This "plain" model has just two direct message types.
 *
 * The real and ideal functionalities should use PKE key pairs associated with
 * the ports that are establishing a session, but since EasyUC lacks global
 * subroutines for setups, an [init_PKE] message provides the PKE keys each role
 * needs. Such infrastructure isn't the point of the model.
 *)

uc_requires Forwarding.
ec_requires +FMap +PKE +PKE_EPDP +NeedhamSchroeder.

(* API for principal A, the initiator of the exchange *)
direct Pt1Dir {
  (* Initializes initiator with its identity, secret key and all public keys *)
  in  pt1@init_PKE (sk_a : sk_t, pk_table : (port, pk_t) fmap)
  out init_PKE_resp@pt1

  (* Requests session with pt2 *)
  in  pt1@ns_req (pt2 : port)
}

(* API for principal B, the responder of the exchange *)
direct Pt2Dir {
  (* Initializes responder with its identity, secret key and all public keys *)
  in  pt2@init_PKE (sk_b : sk_t, pk_table : (port, pk_t) fmap)
  out init_PKE_resp@pt2

  (* Accepts session with pt1 *)
  out ns_acc (pt1 : port)@pt2
}

direct NSDir {
  Pt1D : Pt1Dir
  Pt2D : Pt2Dir
}

functionality NSReal implements NSDir {
  subfun Fwd1 = Forwarding.Forw
  subfun Fwd2 = Forwarding.Forw
  subfun Fwd3 = Forwarding.Forw

  party Pt1 serves NSDir.Pt1D {

    initial state Init {
      match message with
      | pt1@NSDir.Pt1D.init_PKE (sk_a, pk_table) => {
          send NSDir.Pt1D.init_PKE_resp@pt1
          and transition WaitRequest (pt1, sk_a, pk_table).
        }

      | * => { fail. }
      end
    }

    state WaitRequest
            (id_A : port,
             sk_a : sk_t,
             pk_table : (port, pk_t) fmap) {
      var n_A: int;

      match message with
      | pt1@NSDir.Pt1D.ns_req (pt2) => {
          if (pt1 = id_A /\ envport pt2) {
            n_A <$ dnonce;
            match pk_table.[pt2] with
            | Some pk_b => {
                send Fwd1.D.fw_req
                       (intport Pt2,
                        epdp_cipher_univ.`enc
                          (enc pk_b (epdp_int_port_plain.`enc (n_A, id_A))))
                and transition WaitFwd2 (id_A, sk_a, pk_table, pt2, n_A).
              }
            | None => { fail. }
            end
          } else { fail. }
        }

      | * => { fail. }
      end
    }

    state WaitFwd2
            (id_A : port,
             sk_a : sk_t,
             pk_table : (port, pk_t) fmap,
             id_B : port,
             n_A : int) {
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
                    send Fwd3.D.fw_req
                      (intport Pt2,
                       epdp_cipher_univ.`enc
                         (enc (oget pk_table.[id_B]) (epdp_int_plain.`enc n_B)))
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

  party Pt2 serves NSDir.Pt2D {
    initial state Init {
      match message with
      | pt2@NSDir.Pt2D.init_PKE (sk_b, pk_table) => {
          send NSDir.Pt2D.init_PKE_resp@pt2
          and transition WaitFwd1 (pt2, sk_b, pk_table).
        }

      | * => { fail. }
      end
    }

    state WaitFwd1 (id_B : port, sk_b : sk_t, pk_table : (port, pk_t) fmap) {
      var id_A : port;
      var n_A : int;
      var n_B : int;
      var plaintext : ptxt_t;

      match message with
      | Fwd1.D.fw_rsp (_, u) => {
          match epdp_cipher_univ.`dec u with
          | Some ciphertext => {
              plaintext <- dec sk_b ciphertext;
              match epdp_int_port_plain.`dec plaintext with
              | Some ni => {
                  (n_A, id_A) <- ni;
                  n_B <$ dnonce;
                  send Fwd2.D.fw_req
                    (intport Pt1,
                     epdp_cipher_univ.`enc
                       (enc
                          (oget pk_table.[id_A])
                          (epdp_int_int_plain.`enc (n_A, n_B))))
                  and transition WaitFwd3
                        (id_B, sk_b, pk_table, id_A, n_A, n_B).
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

    state WaitFwd3 (id_B : port, sk_b : sk_t, pk_table : (port, pk_t) fmap,
                    id_A : port, n_A : int, n_B : int) {
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
                    send NSDir.Pt2D.ns_acc (id_A)@id_B
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

adversarial NSI2S {
  out init
  out leak (id_A : port, id_B : port, pk_table_a : (port, pk_t) fmap,
            pk_table_b : (port, pk_t) fmap)
  in  ok
}

functionality NSIdeal implements NSDir NSI2S {
  initial state Init {
    match message with
    | pt1@NSDir.Pt1D.init_PKE (_, pk_table_a) => {
        send NSI2S.init
        and transition WaitSim_A (pt1, pk_table_a).
      }

    | pt2@NSDir.Pt2D.init_PKE (_, pk_table_b) => {
        send NSI2S.init
        and transition WaitSim_B (pt2, pk_table_b).
      }

    | * => { fail. }
    end
  }

  state WaitSim_A
          (id_A : port,
           pk_table_a : (port, pk_t) fmap) {
    match message with
    | NSI2S.ok => {
        send NSDir.Pt1D.init_PKE_resp@id_A
        and transition WaitInitPKE_B (id_A, pk_table_a).
      }

    | * => { fail. }
    end
  }

  state WaitSim_B
          (id_B : port,
           pk_table_b : (port, pk_t) fmap) {
    match message with
    | NSI2S.ok => {
        send NSDir.Pt2D.init_PKE_resp@id_B
        and transition WaitInitPKE_A (id_B, pk_table_b).
      }

    | * => { fail. }
    end
  }

  state WaitInitPKE_A
          (id_B : port,
           pk_table_b : (port, pk_t) fmap) {
    match message with
    | pt1@NSDir.Pt1D.init_PKE (_, pk_table_a) => {
        send NSDir.Pt1D.init_PKE_resp@pt1
        and transition WaitRequest (pt1, pk_table_a, id_B, pk_table_b).
      }

    | * => { fail. }
    end
  }

  state WaitInitPKE_B
          (id_A : port,
           pk_table_a : (port, pk_t) fmap) {
    match message with
    | pt2@NSDir.Pt2D.init_PKE (_, pk_table_b) => {
        send NSDir.Pt2D.init_PKE_resp@pt2
        and transition WaitRequest
              (id_A, pk_table_a, pt2, pk_table_b).
      }

    | * => { fail. }
    end
  }

  state WaitRequest
          (id_A : port,
           pk_table_a : (port, pk_t) fmap,
           id_B : port,
           pk_table_b : (port, pk_t) fmap) {
    match message with
    | pt1@NSDir.Pt1D.ns_req (pt2) => {
        if (pt1 <> id_A \/ pt2 <> id_B) { fail. }
        else {
          send NSI2S.leak (pt1, pt2, pk_table_a, pk_table_b)
          and transition WaitSim2 (id_A, id_B).
        }
      }

    | * => { fail. }
    end
  }

  state WaitSim2
          (id_A : port,
           id_B : port) {
    match message with
    | NSI2S.ok => {
        send NSDir.Pt2D.ns_acc (id_A)@id_B
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

simulator NSSim uses NSI2S simulates NSReal {
  initial state WaitInit {
    match message with
    | NSI2S.init => {
        send NSI2S.ok
        and transition WaitIdeal.
      }

    | * => { fail. }
    end
  }

  state WaitIdeal {
    var n_A : int;
    var ciphertext : ctxt_t;

    match message with
    | NSI2S.leak (id_A, id_B, pk_table_a, pk_table_b) => {
        n_A <$ dnonce;
        ciphertext <-
          enc (oget pk_table_a.[id_B]) (epdp_int_port_plain.`enc (n_A, id_A));
        send NSReal.Fwd1.FwAdv.fw_obs
               (intport NSReal.Pt1,
                intport NSReal.Pt2,
                epdp_cipher_univ.`enc ciphertext)
        and transition WaitAdv1
              (id_A, id_B, pk_table_a, pk_table_b, n_A, ciphertext).
      }

    | * => { fail. }
    end
  }

  state WaitAdv1
          (id_A : port,
           id_B : port,
           pk_table_a : (port, pk_t) fmap,
           pk_table_b : (port, pk_t) fmap,
           n_A : int,
           c : ctxt_t) {
    var id_A' : port;
    var id_B' : port;
    var n_B : int;
    var ciphertext : ctxt_t;

    match message with
    | NSReal.Fwd1.FwAdv.fw_ok (pt, u) => {
        if (pt <> intport NSReal.Pt2) {
          fail.
        } else {
          match epdp_cipher_univ.`dec u with
          | Some msg => {
              if (msg <> c) {
                fail.
              } else {
                n_B <$ dnonce;
                ciphertext <-
                  enc (oget pk_table_b.[id_A])
                    (epdp_int_int_plain.`enc (n_A, n_B));
                send NSReal.Fwd2.FwAdv.fw_obs
                       (intport NSReal.Pt2,
                        intport NSReal.Pt1,
                        epdp_cipher_univ.`enc ciphertext)
                and transition WaitAdv2
                      (id_B, n_A, n_B, pk_table_a, ciphertext).
              }
            }
          | None => {
              fail.
            }
          end
        }
      }

    | * => { fail. }
    end
  }

  state WaitAdv2
          (id_B : port,
           n_A : int,
           n_B : int,
           pk_table_a : (port, pk_t) fmap,
           c : ctxt_t) {
    var n_A' : int;
    var n_B' : int;
    var ciphertext : ctxt_t;

    match message with
    | NSReal.Fwd2.FwAdv.fw_ok (pt, u) => {
        if (pt <> intport NSReal.Pt1) {
          fail.
        } else {
          match epdp_cipher_univ.`dec u with
          | Some msg => {
              if (msg <> c) {
                fail.
              } else {
                ciphertext <-
                  enc (oget pk_table_a.[id_B]) (epdp_int_plain.`enc n_B);
                send NSReal.Fwd3.FwAdv.fw_obs
                       (intport NSReal.Pt1,
                        intport NSReal.Pt2,
                        epdp_cipher_univ.`enc ciphertext)
                and transition WaitAdv3 (ciphertext).
              }
            }
          | None => {
              fail.
            }
          end
        }
      }

    | * => { fail. }
    end
  }

  state WaitAdv3 (c : ctxt_t) {
    match message with
    | NSReal.Fwd3.FwAdv.fw_ok (pt, u) => {
        if (pt <> intport NSReal.Pt2) {
          fail.
        } else {
          match epdp_cipher_univ.`dec u with
          | Some msg => {
              if (msg <> c) {
                fail.
              } else {
                send NSI2S.ok
                and transition Final.
              }
            }
          | None => {
              fail.
            }
          end
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
