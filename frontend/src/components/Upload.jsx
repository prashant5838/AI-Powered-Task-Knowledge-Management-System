import React, {useState} from 'react'
import { uploadDocument } from '../api'

export default function Upload({token}){
  const [file,setFile]=useState(null)
  const [msg,setMsg]=useState('')
  async function submit(e){
    e.preventDefault()
    if(!file) return
    const r = await uploadDocument(file, token)
    setMsg(JSON.stringify(r))
  }
  return (
    <div>
      <h4>Upload Document</h4>
      <form onSubmit={submit}>
        <input type="file" onChange={e=>setFile(e.target.files[0])} />
        <button type="submit">Upload</button>
      </form>
      <pre>{msg}</pre>
    </div>
  )
}
