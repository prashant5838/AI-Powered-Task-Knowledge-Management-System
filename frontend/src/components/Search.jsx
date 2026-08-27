import React, {useState} from 'react'
import { search } from '../api'

export default function Search({token}){
  const [q,setQ]=useState('')
  const [res,setRes]=useState(null)
  async function doSearch(e){
    e.preventDefault()
    const r = await search(q, token)
    setRes(r)
  }
  return (
    <div>
      <h4>Search</h4>
      <form onSubmit={doSearch}>
        <input value={q} onChange={e=>setQ(e.target.value)} />
        <button type="submit">Search</button>
      </form>
      <pre>{JSON.stringify(res, null, 2)}</pre>
    </div>
  )
}
