import React from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar.jsx'
import Topbar from './Topbar.jsx'

export default function AppLayout() {
  return (
    <div className="app-layout">
      <Sidebar />
      <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        <Topbar />
        <main
          className="main-content"
          style={{ paddingTop: 8 }}
          id="main-content"
          role="main"
        >
          <Outlet />
        </main>
      </div>
    </div>
  )
}
