import type { Pool } from 'pg';
import { Order, type OrderId, type OrderStatus } from '../../../domain/order';
import type { OrderRepository } from '../../../domain/order-repository';

interface OrderRow {
  customer_id: string;
  status: OrderStatus;
}

export class PostgresOrderRepository implements OrderRepository {
  constructor(private readonly pool: Pool) {}

  async findById(id: OrderId): Promise<Order | null> {
    const { rows } = await this.pool.query<OrderRow>('SELECT customer_id, status FROM orders WHERE id = $1', [id]);
    const row = rows[0];
    return row ? Order.restore({ id, customerId: row.customer_id, status: row.status }) : null;
  }

  async save(order: Order): Promise<void> {
    const s = order.toSnapshot();
    await this.pool.query(
      `INSERT INTO orders (id, customer_id, status) VALUES ($1, $2, $3)
       ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status`,
      [s.id, s.customerId, s.status],
    );
    order.clearEvents();
  }
}
