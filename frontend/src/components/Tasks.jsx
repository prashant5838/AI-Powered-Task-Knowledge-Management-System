import React, {useEffect, useState} from 'react'
import { listTasks, updateTaskStatus } from '../api'

export default function Tasks({token}){
  const [tasks,setTasks]=useState([])
  useEffect(()=>{fetchTasks()},[])
  async function fetchTasks(){
    const r = await listTasks(token)
    setTasks(r)
  }
  async function markDone(id){
    await updateTaskStatus(id,'completed',token)
    fetchTasks()
  }
  return (
    <div>
      <h4>Tasks</h4>
      <ul>
        {tasks.map(t=>(<li key={t.id}>{t.title} - {t.status} <button onClick={()=>markDone(t.id)}>Mark Done</button></li>))}
      </ul>
    </div>
  )
}
