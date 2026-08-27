import React, {useState} from 'react'
import { login } from '../api'

export default function Login({onLogin}){
  const [email,setEmail]=useState('admin@example.com')
  const [pw,setPw]=useState('adminpass')
  const [err,setErr]=useState(null)
  async function submit(e){
    e.preventDefault()
    try{
      const data = await login(email,pw)
      const role = data.role || (data.user && data.user.role) || 'user'
      onLogin(data.access_token, role)
    }catch(e){setErr(String(e))}
  }
  return (
    <form onSubmit={submit}>
      <div><label>Email</label><input value={email} onChange={e=>setEmail(e.target.value)} /></div>
      <div><label>Password</label><input value={pw} onChange={e=>setPw(e.target.value)} type="password"/></div>
      <button type="submit">Login</button>
      {err && <div style={{color:'red'}}>{err}</div>}
    </form>
  )
}
