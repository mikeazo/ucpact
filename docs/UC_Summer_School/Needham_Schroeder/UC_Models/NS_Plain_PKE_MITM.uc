(* In this model, the real functionality is parameterized on two instances of
 * the plain Needham-Schroeder protocol with PKE initialization to enable a
 * demonstration of the man-in-the-middle attack in an interpreter script.
 *
 * The ideal and simulator don't do anything; they are vestigial, to make the
 * type checker happy.
 *)

uc_requires NeedhamSchroederPlainPKE.
ec_requires +FMap +PKE +PKE_EPDP +NeedhamSchroeder.

(* Interface for the principal A *)
direct PtADir {
  (* Initializes the party of the first NS instance that represents A *)
  in  pt@init_PKE
        (sk_A : sk_t,
         pk_table : (port, pk_t) fmap)

  (* Initiates the session between A and I *)
  in  pt@part1

  (* Common response *)
  out ok@pt
}

(* Interface for the principal B *)
direct PtBDir {
  (* Initializes the party of the second NS instance that represents B *)
  in  pt@init_PKE
        (sk_B : sk_t,
         pk_table : (port, pk_t) fmap)

  (* Common response *)
  out ok@pt
}

(* Interface for the principal I, for Intruder (the adversary) *)
direct PtIDir {
  (* Initializes the parties of the two NS instances that represent I *)
  in  pt@init_PKE
        (sk_I : sk_t,
         pk_table : (port, pk_t) fmap)

  (* Initiates the session between I and B, where I impersonates A *)
  in  pt@part2

  (* Common response *)
  out ok@pt
}

(* Composite direct interface *)
direct NSMITMDir {
  PtAD : PtADir
  PtBD : PtBDir
  PtID : PtIDir
}

(* Real Functionality *)
functionality NSMITMReal
  (NS1 : NeedhamSchroederPlainPKE.NSDir,
   NS2 : NeedhamSchroederPlainPKE.NSDir) implements NSMITMDir {

  (* This party is the principal A with respect to the two parameters *)
  party A serves NSMITMDir.PtAD {

    (* Initializes the agent for principal A (NS1.Pt1) with its identity (which
     * is the port of this party), secret key and table of public keys *)
    initial state Initialize {
      match message with
      | pt@NSMITMDir.PtAD.init_PKE (sk_A, pk_table) => {
          send NS1.Pt1D.init_PKE (sk_A, pk_table)
          and transition WaitNS1 (pt).
        }

      | * => { fail. }
      end
    }

    state WaitNS1 (respPort : port) {
      match message with
      | NS1.Pt1D.init_PKE_resp => {
          send NSMITMDir.PtAD.ok@respPort
          and transition Part1.
        }

      | * => { fail. }
      end
    }

    state Part1 {
      match message with
      | pt@NSMITMDir.PtAD.part1 => {
          send NS1.Pt1D.ns_req (intport I)
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

  (* This party is the principal B with respect to the two parameters *)
  party B serves NSMITMDir.PtBD {

    (* Initializes the agent for principal B (NS2.Pt2) with its identity (which
     * is the port of this party), secret key and table of public keys *)
    initial state Initialize {
      match message with
      | pt@NSMITMDir.PtBD.init_PKE (sk_B, pk_table) => {
          send NS2.Pt2D.init_PKE (sk_B, pk_table)
          and transition WaitNS2Init (pt).
        }

      | * => { fail. }
      end
    }

    state WaitNS2Init (respPort : port) {
      match message with
      | NS2.Pt2D.init_PKE_resp => {
          send NSMITMDir.PtBD.ok@respPort
          and transition WaitNS2Accept (respPort).
        }

      | * => { fail. }
      end
    }

    state WaitNS2Accept (respPort : port) {
      match message with
      | NS2.Pt2D.ns_acc (_) => {
          send NSMITMDir.PtBD.ok@respPort
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

  (* This party is the principal I with respect to the two parameters *)
  party I serves NSMITMDir.PtID {

    (* Initializes the agents for principal I (NS1.Pt2 & NS2.Pt1) with their
     * identities (which are the port of this party), secret key and table of
     * public keys *)
    initial state Initialize {
      match message with
      | pt@NSMITMDir.PtID.init_PKE (sk_I, pk_table) => {
          send NS1.Pt2D.init_PKE (sk_I, pk_table)
          and transition WaitNS1Init (pt, sk_I, pk_table).
        }

      | * => { fail. }
      end
    }

    state WaitNS1Init
            (respPort : port,
             sk_I : sk_t,
             pk_table : (port, pk_t) fmap) {
      match message with
      | NS1.Pt2D.init_PKE_resp => {
          send NS2.Pt1D.init_PKE (sk_I, pk_table)
          and transition WaitNS2Init (respPort).
        }

      | * => { fail. }
      end
    }

    state WaitNS2Init (respPort : port) {
      match message with
      | NS2.Pt1D.init_PKE_resp => {
          send NSMITMDir.PtID.ok@respPort
          and transition Part2.
        }

      | * => { fail. }
      end
    }

    state Part2 {
      match message with
      | pt@NSMITMDir.PtID.part2 => {
          send NS2.Pt1D.ns_req (intport B)
          and transition WaitNS1Accept (pt).
        }

      | * => { fail. }
      end
    }

    state WaitNS1Accept (respPort : port) {
      match message with
      | NS1.Pt2D.ns_acc (_) => {
          send NSMITMDir.PtID.ok@respPort
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
}

adversarial NSMITMI2S {
  out leak
  in  ok
}

(* Ideal functionality *)
functionality NSMITMIdeal implements NSMITMDir NSMITMI2S {

  initial state InitState {
    match message with

    | * => { fail. }
    end
  }
}

(* Simulator *)
simulator NSMITMSim uses NSMITMI2S
  simulates NSMITMReal
    (NeedhamSchroederPlainPKE.NSIdeal, NeedhamSchroederPlainPKE.NSIdeal) {

  initial state InitState {
    match message with

    | * => { fail. }
    end
  }
}

