import React, {useState, useEffect} from 'react'
import Login from './components/Login'
import Upload from './components/Upload'
import Tasks from './components/Tasks'
import Search from './components/Search'
import { getCurrentUser } from './api'

export default function App(){
  const [token, setToken] = useState(() => localStorage.getItem('token'))
  const [role, setRole] = useState(() => localStorage.getItem('role'))
  const [user, setUser] = useState(null)

  useEffect(()=>{
    async function load(){
      if(token){
        try{
          const data = await getCurrentUser(token)
          setRole(data.role)
          setUser(data.user)
          localStorage.setItem('role', data.role)
        }catch(e){
          console.error('Auth load failed', e)
          setToken(null)
          localStorage.removeItem('token')
          localStorage.removeItem('role')
        }
      }
    }
    load()
  }, [token])
  return (
    <div style={{padding:20}}>
      {!token ? <Login onLogin={(t,r)=>{setToken(t); setRole(r); localStorage.setItem('token', t); localStorage.setItem('role', r);}} /> : (
        <>
          <h3>AI Task & Knowledge MVP</h3>
          {role === 'admin' && <Upload token={token} />}
          <Search token={token} />
          <Tasks token={token} />
          <div style={{marginTop:10}}>
            <button onClick={()=>{setToken(null); setRole(null); localStorage.removeItem('token'); localStorage.removeItem('role')}}>Logout</button>
          </div>
        </>
      )}
    </div>
  )
}
