const API = (path) => `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}${path}`

export async function login(email, password){
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', password)
  const r = await fetch(API('/auth/login'), {method:'POST', body: form})
  if(!r.ok) throw new Error('Login failed')
  return r.json()
}

export async function uploadDocument(file, token){
  const fd = new FormData()
  fd.append('file', file)
  const r = await fetch(API('/documents/upload'), {method:'POST', body: fd, headers: {Authorization: `Bearer ${token}`}})
  return r.json()
}

export async function search(q, token){
  const r = await fetch(API(`/search?q=${encodeURIComponent(q)}`), {headers:{Authorization:`Bearer ${token}`}})
  return r.json()
}

export async function getCurrentUser(token){
  const r = await fetch(API('/auth/me'), {headers:{Authorization:`Bearer ${token}`}})
  if(!r.ok) throw new Error('Not authenticated')
  return r.json()
}

export async function listTasks(token){
  const r = await fetch(API('/tasks'), {headers:{Authorization:`Bearer ${token}`}})
  return r.json()
}

export async function createTask(payload, token){
  const r = await fetch(API('/tasks'), {method:'POST', headers:{'Content-Type':'application/json', Authorization:`Bearer ${token}`}, body:JSON.stringify(payload)})
  return r.json()
}

export async function updateTaskStatus(id, status, token){
  const r = await fetch(API(`/tasks/${id}/status?status=${encodeURIComponent(status)}`), {method:'PATCH', headers:{Authorization:`Bearer ${token}`}})
  return r.json()
}
