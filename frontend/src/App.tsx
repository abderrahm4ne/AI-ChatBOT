import { useState, useMemo } from 'react'
import SimpleChat from './components/SimpleChat'

type ChatMessage = {
  role: 'user' | 'assistant'
  content: string
}


function App() {

  return (
    <div className='h-[100vh] bg-gradient-to-r from-cyan-800 to-cyan-700 flex items-center justify-center'>
      <SimpleChat />
    </div>
  )
}

export default App