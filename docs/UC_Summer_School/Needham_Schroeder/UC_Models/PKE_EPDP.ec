(* EPDPs for PKE
 *
 * NOTE: This file requires files located in <EasyUC path>/uc-dsl/prelude.
 *)

require import PKE UCUniv.
(*---*) import UCEncoding.

(* ctxt_t <=> univ *)
op [opaque smt_opaque] epdp_cipher_univ : (ctxt_t, univ) epdp.
axiom valid_epdp_cipher_univ : valid_epdp epdp_cipher_univ.
hint simplify valid_epdp_cipher_univ.

(* ptxt_t * ptxt_t <=> ptxt_t *)
op [opaque smt_opaque] epdp_plain_pair_plain : (ptxt_t * ptxt_t, ptxt_t) epdp.
axiom valid_epdp_plain_pair_plain : valid_epdp epdp_plain_pair_plain.
hint simplify valid_epdp_plain_pair_plain.

(* ptxt_t * ptxt_t * ptxt_t <=> ptxt_t *)
op [opaque smt_opaque] enc_plain_tuple3 (t : ptxt_t * ptxt_t * ptxt_t)
  : ptxt_t =
  epdp_plain_pair_plain.`enc (t.`1, (epdp_plain_pair_plain.`enc (t.`2, t.`3))).

op [opaque smt_opaque] dec_plain_tuple3 (u : ptxt_t)
  : (ptxt_t * ptxt_t * ptxt_t) option =
  match epdp_plain_pair_plain.`dec u with
  | None   => None
  | Some p =>
      match epdp_plain_pair_plain.`dec p.`2 with
        None   => None
      | Some q => Some (p.`1, q.`1, q.`2)
      end
  end.

op [opaque smt_opaque] epdp_plain_tuple3_plain
  : (ptxt_t * ptxt_t * ptxt_t, ptxt_t) epdp =
  {|enc = enc_plain_tuple3; dec = dec_plain_tuple3|}.

lemma valid_epdp_plain_tuple3_plain : valid_epdp epdp_plain_tuple3_plain.
proof.
apply epdp_intro => [x | u x].
rewrite /epdp_plain_tuple3_plain /= /enc_plain_tuple3 /dec_plain_tuple3 /=.
by case x.
rewrite /epdp_plain_tuple3_plain /= /enc_plain_tuple3 /dec_plain_tuple3 =>
  match_dec_u_eq_some.
have val_u :
  epdp_plain_pair_plain.`dec u =
  Some (x.`1, epdp_plain_pair_plain.`enc (x.`2, x.`3)).
  move : match_dec_u_eq_some.
  case (epdp_plain_pair_plain.`dec u) => // [[]] x1 q /=.
  move => match_dec_q_eq_some.
  have val_y2 :
    epdp_plain_pair_plain.`dec q = Some (x.`2, x.`3).
    move : match_dec_q_eq_some.
    case (epdp_plain_pair_plain.`dec q) => // [[]] x2 x3 /= <- //.
  move : match_dec_q_eq_some.
  rewrite val_y2 /= => <- /=.
  rewrite (epdp_dec_enc _ _ q) 1:valid_epdp_plain_pair_plain //.
by rewrite (epdp_dec_enc _ _ u) 1:valid_epdp_plain_pair_plain.
qed.

hint simplify valid_epdp_plain_tuple3_plain.
hint rewrite epdp : valid_epdp_plain_tuple3_plain.

(* ptxt_t * ptxt_t * ptxt_t * ptxt_t <=> ptxt_t *)
op [opaque smt_opaque] enc_plain_tuple4 (t : ptxt_t * ptxt_t * ptxt_t * ptxt_t)
  : ptxt_t =
  epdp_plain_pair_plain.`enc
    (t.`1, (epdp_plain_tuple3_plain.`enc (t.`2, t.`3, t.`4))).

op [opaque smt_opaque] dec_plain_tuple4 (u : ptxt_t)
  : (ptxt_t * ptxt_t * ptxt_t * ptxt_t) option =
  match epdp_plain_pair_plain.`dec u with
  | None   => None
  | Some p =>
      match epdp_plain_tuple3_plain.`dec p.`2 with
        None   => None
      | Some q => Some (p.`1, q.`1, q.`2, q.`3)
      end
  end.

op [opaque smt_opaque] epdp_plain_tuple4_plain
  : (ptxt_t * ptxt_t * ptxt_t * ptxt_t, ptxt_t) epdp =
  {|enc = enc_plain_tuple4; dec = dec_plain_tuple4|}.

lemma valid_epdp_plain_tuple4_plain : valid_epdp epdp_plain_tuple4_plain.
proof.
apply epdp_intro => [x | u x].
rewrite /epdp_plain_tuple4_plain /= /enc_plain_tuple4 /dec_plain_tuple4 /=.
by case x.
rewrite /epdp_plain_tuple4_plain /= /enc_plain_tuple4 /dec_plain_tuple4 =>
  match_dec_u_eq_some.
have val_u :
  epdp_plain_pair_plain.`dec u =
  Some (x.`1, epdp_plain_tuple3_plain.`enc (x.`2, x.`3, x.`4)).
  move : match_dec_u_eq_some.
  case (epdp_plain_pair_plain.`dec u) => // [[]] x1 q /=.
  move => match_dec_q_eq_some.
  have val_y2 :
    epdp_plain_tuple3_plain.`dec q = Some (x.`2, x.`3, x.`4).
    move : match_dec_q_eq_some.
    case (epdp_plain_tuple3_plain.`dec q) => // [[]] x2 x3 x4 /= <- //.
  move : match_dec_q_eq_some.
  rewrite val_y2 /= => <- /=.
  rewrite (epdp_dec_enc _ _ q) 1:valid_epdp_plain_tuple3_plain //.
by rewrite (epdp_dec_enc _ _ u) 1:valid_epdp_plain_pair_plain.
qed.

hint simplify valid_epdp_plain_tuple4_plain.
hint rewrite epdp : valid_epdp_plain_tuple4_plain.

