import React, { useState } from 'react'

const orders = [
  { id: 'ORD-10421', customer: 'Rina Hartono', email: 'rina.hartono@example.com', total: 1249000, status: 'Paid', date: '2026-10-21' },
  { id: 'ORD-10422', customer: 'Budi Santoso', email: 'budi@example.com', total: 89000, status: 'Pending', date: '2026-10-21' },
  { id: 'ORD-10423', customer: 'PT Sinar Jaya Abadi Logistik Nusantara', email: 'procurement.team@sinarjaya-logistik.co.id', total: 15780000, status: 'Paid', date: '2026-10-22' },
  { id: 'ORD-10424', customer: 'Dewi Lestari', email: 'dewi.l@example.com', total: 432500, status: 'Refunded', date: '2026-10-22' },
  { id: 'ORD-10425', customer: 'Agus Wijaya', email: 'agus.w@example.com', total: 2100000, status: 'Failed', date: '2026-10-23' },
  { id: 'ORD-10426', customer: 'Siti Nurhaliza', email: 'siti@example.com', total: 675000, status: 'Paid', date: '2026-10-24' },
]

function fmt(n) { return 'Rp ' + n.toLocaleString('id-ID') }

export default function App() {
  const [tab, setTab] = useState('orders')
  const [q, setQ] = useState('')
  const rows = orders.filter(o => o.customer.toLowerCase().includes(q.toLowerCase()))
  return (
    <div style={{ display: 'flex', fontFamily: 'Arial', background: '#f3f3f3', minHeight: '100vh' }}>
      <div className="sidebar">
        <h2 style={{ color: '#fff', padding: '18px 15px', margin: 0, fontSize: '21px' }}>ACME Admin</h2>
        {['dashboard', 'orders', 'customers', 'products', 'settings'].map(t => (
          <div key={t} onClick={() => setTab(t)} className={tab === t ? 'nav active' : 'nav'} style={{ padding: '11px 17px', textTransform: 'capitalize' }}>{t}</div>
        ))}
      </div>
      <div style={{ flex: 1, padding: '25px 30px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1 style={{ fontSize: '27px', color: '#222', margin: '0 0 22px' }}>Orders</h1>
          <button className="btn" style={{ background: 'linear-gradient(90deg,#7b2ff7,#f107a3)', borderRadius: '20px' }}>+ New Order</button>
        </div>
        <div className="stats">
          <div className="stat" style={{ background: '#e8f4ff' }}><div style={{ color: '#888', fontSize: '13px' }}>Revenue (Oct)</div><div style={{ fontSize: '26px', fontWeight: 'bold', color: '#1a73e8' }}>Rp 20.345.500</div><div style={{ color: 'green', fontSize: '12px' }}>▲ 12.4%</div></div>
          <div className="stat" style={{ background: '#fff4e5' }}><div style={{ color: '#999', fontSize: '12px' }}>Orders</div><div style={{ fontSize: '28px', fontWeight: '800', color: '#ff8c00' }}>6</div><div style={{ color: 'red', fontSize: '11px' }}>▼ 3%</div></div>
          <div className="stat" style={{ background: '#e9fbe9' }}><div style={{ color: '#777', fontSize: '14px' }}>Customers</div><div style={{ fontSize: '24px', fontWeight: 'bold', color: '#2e7d32' }}>6</div></div>
          <div className="stat" style={{ background: '#fdeaea' }}><div style={{ color: '#aaa', fontSize: '13px' }}>Refund rate</div><div style={{ fontSize: '25px', fontWeight: 'bold', color: '#d32f2f' }}>16.7%</div></div>
        </div>
        <input placeholder="search..." value={q} onChange={e => setQ(e.target.value)} style={{ padding: '7px 9px', border: '1px solid #ccc', borderRadius: '3px', width: '260px', margin: '18px 0 13px', outline: 'none' }} />
        <table className="tbl">
          <thead><tr><th>Order</th><th>Customer</th><th>Total</th><th>Status</th><th>Date</th><th></th></tr></thead>
          <tbody>
            {rows.map(o => (
              <tr key={o.id}>
                <td style={{ color: '#1a73e8' }}>{o.id}</td>
                <td><b>{o.customer}</b><br /><span style={{ color: '#aaa', fontSize: '11px' }}>{o.email}</span></td>
                <td>{fmt(o.total)}</td>
                <td><span className={'badge ' + o.status.toLowerCase()}>{o.status}</span></td>
                <td style={{ color: '#999' }}>{o.date}</td>
                <td><button style={{ background: 'none', border: '1px solid #ddd', padding: '4px 10px', borderRadius: '6px', cursor: 'pointer' }}>View</button> <button style={{ background: '#ff4d4f', color: 'white', border: 'none', padding: '5px 9px', borderRadius: '4px' }}>Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
