import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { spawn } from 'child_process'
import net from 'net'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

function autoStartBackendPlugin() {
  return {
    name: 'auto-start-backend',
    configureServer() {
      const socket = new net.Socket()
      socket.setTimeout(1000)
      socket.once('connect', () => {
        socket.destroy()
        console.log('\x1b[32m✓ FastAPI Backend is already active on http://127.0.0.1:8000\x1b[0m')
      })
      socket.once('error', () => {
        socket.destroy()
        console.log('\x1b[36m🚀 Auto-starting FastAPI Backend on http://127.0.0.1:8000 ...\x1b[0m')
        const backendDir = path.resolve(__dirname, '../backend')
        const pythonExe = process.platform === 'win32'
          ? path.join(backendDir, 'venv', 'Scripts', 'python.exe')
          : path.join(backendDir, 'venv', 'bin', 'python')
        const proc = spawn(pythonExe, ['-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000'], {
          cwd: backendDir,
          stdio: 'inherit',
          shell: false
        })
        proc.on('error', (err) => {
          console.error('Failed to auto-start backend:', err.message)
        })
      })
      socket.connect(8000, '127.0.0.1')
    }
  }
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), autoStartBackendPlugin()],
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
})
