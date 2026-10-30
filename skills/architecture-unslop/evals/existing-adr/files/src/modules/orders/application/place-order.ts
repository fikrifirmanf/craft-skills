import { Order, type OrderId } from '../domain/order';
import type { OrderRepository } from '../domain/order-repository';

export interface PlaceOrderCommand {
  readonly orderId: OrderId;
  readonly customerId: string;
}

export class PlaceOrder {
  constructor(
    private readonly orders: OrderRepository,
    private readonly now: () => Date,
  ) {}

  async execute(cmd: PlaceOrderCommand): Promise<{ orderId: OrderId }> {
    const existing = await this.orders.findById(cmd.orderId);
    if (existing) return { orderId: existing.id };
    const order = Order.draft(cmd.orderId, cmd.customerId);
    order.place(this.now());
    await this.orders.save(order);
    return { orderId: order.id };
  }
}
