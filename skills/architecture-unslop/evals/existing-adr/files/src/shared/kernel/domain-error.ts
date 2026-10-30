export class DomainError extends Error {
  constructor(readonly code: string) {
    super(code);
  }
}
