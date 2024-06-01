import { serve } from '@hono/node-server'
import { existsSync } from 'fs'
import { readFile } from 'fs/promises'
import { Hono } from 'hono'

const app = new Hono()

app.get('/', async (c) => {
  const file = (await readFile('./index.html')).toString()
  return c.html(file)
})

app.get('/style.css', async (c) => {
  const file = (await readFile('./style.css')).toString()
  c.header('content-type', 'text/css')
  return c.body(Buffer.from(file))
})

app.get('/origin/:num', async (c) => {
  const { num } = c.req.param();
  const fn = `../frames/${num}.png`;

  if (!existsSync(fn)) {
    c.status(404)
    return c.text('Not Found')
  }

  const img = await readFile(fn);
  
  c.status(200)
  c.header('Content-Type', 'image/png');
  return c.body(img)
})

app.get('/aw-bnuy/:num', async (c) => {
  const { num } = c.req.param();
  const fn = `../bnuy_frames/${num}.png`;

  if (!existsSync(fn)) {
    c.status(404)
    return c.text('Not Found')
  }

  const img = await readFile(fn);
  
  c.status(200)
  c.header('Content-Type', 'image/png');
  return c.body(img)
})

const port = 3000
console.log(`Server is running on port ${port}`)

serve({
  fetch: app.fetch,
  port
})
