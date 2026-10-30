import { DomainError } from '../../../shared/kernel/domain-error';
import type { OrderPlaced } from './order-events';

export type OrderId = string & { readonly __brand: 'OrderId' };
export type OrderStatus = 'draft' | 'placed' | 'shipped';

export interface OrderSnapshot {
  readonly id: OrderId;
  readonly customerId: string;
  readonly status: OrderStatus;
}

export class Order {
  private pending: OrderPlaced[] = [];

  private constructor(
    readonly id: OrderId,
    readonly customerId: string,
    private status: OrderStatus,
  ) {}

  static draft(id: OrderId, customerId: string): Order {
    return new Order(id, customerId, 'draft');
  }

  static restore(s: OrderSnapshot): Order {
    return new Order(s.id, s.customerId, s.status);
  }

  place(at: Date): void {
    if (this.status !== 'draft') throw new DomainError('ORDER_NOT_DRAFT');
    this.status = 'placed';
    this.pending.push({ type: 'OrderPlaced', orderId: this.id, occurredAt: at });
  }

  ship(): void {
    if (this.status !== 'placed') throw new DomainError('ORDER_NOT_PLACED');
    this.status = 'shipped';
  }

  pendingEvents(): readonly OrderPlaced[] {
    return this.pending;
  }

  clearEvents(): void {
    this.pending = [];
  }

  toSnapshot(): OrderSnapshot {
    return { id: this.id, customerId: this.customerId, status: this.status };
  }
}
