import type { OrderId } from './order';

export interface OrderPlaced {
  readonly type: 'OrderPlaced';
  readonly orderId: OrderId;
  readonly occurredAt: Date;
}
