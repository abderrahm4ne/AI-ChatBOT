import { useState, useMemo } from 'react'
import SimpleChat from './components/SimpleChat'

type ChatMessage = {
  role: 'user' | 'assistant'
  content: string
}


function App() {

  return (
    <div className='bg-gradient-to-r from-cyan-800 to-cyan-700 flex justify-center p-6'>
      <SimpleChat />
    </div>
  )
}

export default App