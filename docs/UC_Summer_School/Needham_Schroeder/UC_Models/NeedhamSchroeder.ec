(* Support theory for the Needham-Schroeder protocol
 *
 * NOTE: This file requires files located in <EasyUC path>/uc-dsl/prelude.
 *)

require import Core Distr FMap Int PKE PKE_EPDP UCBasicTypes.

(* FMap hints *)
hint simplify emptyE, filter_empty, get_setE, map_empty, map_set, set_set_sameE.

(* RNG for nonces *)
op dnonce : int distr = drange 0 18446744073709551616. (* 2^64 *)

(* EPDPs *)

(* port & port & ctxt_t <=> univ *)
op [opaque smt_opaque] epdp_port_port_cipher_univ :
  (port * port * ctxt_t, univ) epdp =
  epdp_tuple3_univ epdp_port_univ epdp_port_univ epdp_cipher_univ.
lemma valid_epdp_port_port_cipher_univ : valid_epdp epdp_port_port_cipher_univ
  by rewrite /epdp_port_port_cipher_univ.
hint simplify valid_epdp_port_port_cipher_univ.

(* port <=> ptxt_t *)
op [opaque smt_opaque] epdp_port_plain : (port, ptxt_t) epdp.
axiom valid_epdp_port_plain : valid_epdp epdp_port_plain.
hint simplify valid_epdp_port_plain.

(* pk_t <=> ptxt_t *)
op [opaque smt_opaque] epdp_pk_plain : (pk_t, ptxt_t) epdp.
axiom valid_epdp_pk_plain : valid_epdp epdp_pk_plain.
hint simplify valid_epdp_pk_plain.

(* int <=> ptxt_t *)
op [opaque smt_opaque] epdp_int_plain : (int, ptxt_t) epdp.
axiom valid_epdp_int_plain : valid_epdp epdp_int_plain.
hint simplify valid_epdp_int_plain.

(* int & int <=> ptxt_t *)
op [opaque smt_opaque] epdp_int_int_plain : (int * int, ptxt_t) epdp =
  epdp_comp epdp_plain_pair_plain (epdp_pair epdp_int_plain epdp_int_plain).
lemma valid_epdp_int_int_plain : valid_epdp epdp_int_int_plain
  by rewrite /epdp_int_int_plain valid_epdp_comp.
hint simplify valid_epdp_int_int_plain.

(* int & port <=> ptxt_t *)
op [opaque smt_opaque] epdp_int_port_plain : (int * port, ptxt_t) epdp =
  epdp_comp epdp_plain_pair_plain (epdp_pair epdp_int_plain epdp_port_plain).
lemma valid_epdp_int_port_plain : valid_epdp epdp_int_port_plain
  by rewrite /epdp_int_port_plain valid_epdp_comp.
hint simplify valid_epdp_int_port_plain.

(* port & int <=> ptxt_t *)
op [opaque smt_opaque] epdp_port_int_plain : (port * int, ptxt_t) epdp =
  epdp_comp epdp_plain_pair_plain (epdp_pair epdp_port_plain epdp_int_plain).
lemma valid_epdp_port_int_plain : valid_epdp epdp_port_int_plain
  by rewrite /epdp_port_int_plain valid_epdp_comp.
hint simplify valid_epdp_port_int_plain.

(* int & int & port <=> ptxt_t *)
op [opaque smt_opaque] epdp_int_int_port_plain : (int * int * port, ptxt_t) epdp =
  epdp_comp epdp_plain_tuple3_plain (epdp_tuple3 epdp_int_plain
    epdp_int_plain epdp_port_plain).
lemma valid_epdp_int_int_port_plain : valid_epdp epdp_int_int_port_plain
  by rewrite /epdp_int_int_port_plain valid_epdp_comp.
hint simplify valid_epdp_int_int_port_plain.
