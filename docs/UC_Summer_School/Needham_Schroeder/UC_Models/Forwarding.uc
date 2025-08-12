(* Model of message transmission over a network under adversarial control.
 * Each instance sends at most one message.
 *
 * This is a singleton unit consisting only of an ideal functionality. The
 * adversary is able to observe and delay messages and change the message and/or
 * the recipient, but not the sender.
 *)

direct FwDir' {
  (* message from pt1, requesting to send u to pt2 *)
  in  pt1@fw_req (pt2 : port, u : univ)

  (* message to pt2, saying that pt1 sent u to it *)
  out fw_rsp (pt1 : port, u : univ)@pt2
}

direct FwDir {
  D : FwDir'
}

adversarial FwAdv {
  (* Informs adversary that [pt1] wants to send [u] to [pt2] *)
  out fw_obs (pt1 : port, pt2 : port, u : univ)

  (* Allows delivery of [u] to recipient [pt2] *)
  in  fw_ok (pt2 : port, u : univ)
}

functionality Forw implements FwDir FwAdv {
  initial state Init {
    match message with
    | pt1@FwDir.D.fw_req (pt2, u) => {
        if (envport pt2) {
          send FwAdv.fw_obs (pt1, pt2, u)
          and transition Wait (pt1).
        }
        else { fail. }
      }
    end
  }

  state Wait (pt1 : port) {
    match message with
    | FwAdv.fw_ok (pt2, u) => {
        send FwDir.D.fw_rsp (pt1, u)@pt2
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
