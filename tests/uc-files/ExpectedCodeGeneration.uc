(* You have made use of other models in this model. You must include the following:
 * uc_requires BasicModel BasicModel.
 *)

(* Basic direct interface *)
direct Basic1 {
   in pt@message1(param1 : type1)   out message2(param2 : type2)@pt
}

(* Basic adversarial interface *)
adversarial BasicAdv1 {
   in message3(param3 : type3)   out message4(param4 : type4)
}

(* Basic adversarial interface *)
adversarial IFAdvInter {

}

(* Basic adversarial interface *)
adversarial SimAdvInter {

}

(* Composite direct interface *)
direct Comp1 {
   BasicInt1 : Basic1
}

(* Composite adversarial interface *)
adversarial CompAdv1 {
   BasicInt2 : BasicAdv1
}

(* Real Functionality *)
functionality Real_Functionality(Param1 : BasicModel.CompDir1) implements Comp1 CompAdv1 {

  (* Subfunctionalites *)
  subfun Sub1 = BasicModel.IF

  (* Party *)
  party Party1 serves Comp1.BasicInt1 CompAdv1.BasicInt2 {
    initial state InitState {
      match message with 
        | pt@Comp1.BasicInt1.message1(param1) => {
            send Comp1.BasicInt1.message2(val2)@pt
            and transition State1(val1).
        }
        | Sub1.BasicInt1.message2(param2) => {
            send Sub1.BasicInt1.message1(val1)
            and transition State1(val1).
        }
        | Param1.BasicInt1.message2(param2) => {
            send Param1.BasicInt1.message1(val1)
            and transition State1(val1).
        }

        | * => { fail. }
      end
    }

    state State1(param1 : type1) {
      match message with

        | * => { fail. }
      end
    }

  }

}

(* Ideal functionality *)
functionality IF implements Comp1 IFAdvInter {

  initial state InitState {
    match message with
      | pt@Comp1.BasicInt1.message1(param1) => {
          send Comp1.BasicInt1.message2(val2)@pt
          and transition State2(val2).
      }


      | * => { fail. }
    end
  }

  state State2(param2 : type2) {
    match message with

      | * => { fail. }
    end
  }

}

(* Simulator *)
simulator Sim uses SimAdvInter simulates Real_Functionality(BasicModel.IF) {

  initial state InitState {
    match message with
      | BasicAdv1.message3(param3) => {
          send BasicAdv1.message4(val4)
          and transition State1(val1).
      }

      | * => { fail. }
    end
  }

  state State1(param1 : type1) {
    match message with

      | * => { fail. }
    end
  }

}

