(* Support theory for public key encryption
 *
 * Adapted from PublicKeyEncryption.eca in easycrypt/lib/theories/crypto
 * A key difference is that [ctxt_t] and [ptxt_t] are the same type, so that
 * any text can be signed by decoding it with a secret key and so on.
 *
 * NOTE: This file requires files located in <EasyUC path>/uc-dsl/prelude.
 *)
 
require import UCBasicTypes.

(** Public keys **)
type pk_t.

(** Secret keys **)
type sk_t.

(** Plaintexts/messages **)
type ptxt_t.

(** Ciphertexts/signatures **)
type ctxt_t = ptxt_t.

op enc (pk: pk_t, p: ptxt_t): ctxt_t.
op dec (sk: sk_t, c: ctxt_t): ptxt_t.

op gen_pair : pk_t -> sk_t -> bool.

axiom pk_enc_dec sk pk p :
  gen_pair pk sk => dec sk (enc pk p) = p.

axiom pk_dec_enc sk pk c :
  gen_pair pk sk => enc pk (dec sk c) = c.

(* hint simplify pk_enc_dec, pk_dec_enc. *)
hint rewrite ucdsl_interpreter_hints : pk_enc_dec pk_dec_enc.

