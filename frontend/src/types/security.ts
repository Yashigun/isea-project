export type BlockReason =
  | "brute_force"
  | "credential_stuffing"
  | "sql_injection"
  | "xss"
  | "bot"
  | "rate_limit"
  | "manual"
  | "other";