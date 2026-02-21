import { v4 as uuidv4 } from 'uuid'
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import SendIcon from '@mui/icons-material/Send';
import { useState, useMemo } from 'react'
import CircularProgress from '@mui/material/CircularProgress';

export default function SimpleChat(){

type Message = {
    role: 'user' | 'ai',
    content: string
}   

    const threadID = useMemo(() => (uuidv4()), []);

    const [message, setMessage] = useState<string>('')
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [chatHistory, setChatHistory] = useState<Message[]>([]);

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files[0];
        if(!selectedFile) return
        
        const formData = new FormData()
        formData.append("file", selectedFile)
        setIsLoading(true)
        try{
            const response = await fetch('http://localhost:8000/upload-pdf', {
                method: 'POST',
                body: formData
            })
            alert("PDF has been sent to the agent")
        }
        catch(error){
            console.error("Error Occured", error)
        }
        finally{
            setIsLoading(false)
        }
    }

    const handleSendMessage = async () => {
        if(!message.trim()) return alert('you must enter a question')
        
        const userPrompt: Message = { role: 'user', content: message }
        setChatHistory(prev => [...prev, userPrompt]);
        setMessage("")

        try{
            const response = await fetch("http://localhost:8000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    query: userPrompt,
                    thread_id: threadID
                })
            })
            const data = await response.json()

            setChatHistory(prev => [...prev, { role: 'ai', content: data.response}])
        }
        catch(error){
            console.error("Error occured while sending message", error)
        }
    }

    return(
        <div className="p-2 px-4 max-w-2xl mx-auto space-y-4 bg-slate-800 flex flex-col rounded-xl min-w-140">

            <div className='flex flex-col gap-0.2'>
                <h3 className='font-bold text-blue-300 '>RAG AI ChatBOT</h3>
                <p className='text-sm text-gray-400'>Thread id : {threadID}</p>
            </div>

            <div className='flex flex-col'>

                <Button
                    component="label"
                    role={undefined}
                    variant="contained"
                    startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <CloudUploadIcon />}
                    disabled={isLoading}
                    tabIndex={-1}
                    sx={{
                        backgroundColor: "#67b3d9",
                        "&:hover": {
                            backgroundColor: "#5fa5c7"
                        },
                        "&:active": {
                            backgroundColor: "#4f92b5"
                        }
                    }}
                >
                    <input type="file" hidden onChange={handleFileUpload} accept=".pdf" />
                </Button>

            </div>

            <main className='border-1 border-[#67b3d9] rounded-md p-1 min-h-100 overflow-y bg-slate-900'>
                <div className='border border-[#67b3d9] rounded-md p-4 h-96 overflow-y-auto bg-slate-900 text-white flex flex-col gap-3'>
                {chatHistory.map((msg, i) => (
                    <div key={i} className={`p-2 rounded-lg max-w-[80%] ${msg.role === 'user' ? 'bg-blue-600 self-end' : 'bg-slate-700 self-start'}`}>
                        {msg.content}
                    </div>
                ))}
                </div>
            </main>

            <div className='flex flex-col gap-1'>
                <TextField
                    label="Write your question here.."
                    onChange={(e) => setMessage(e.target.value)}
                    multiline
                    rows={4}
                    sx={{
                        "& .MuiOutlinedInput-root": {
                            "& fieldset": {
                                borderColor: "#67b3d9",
                            },
                            "&:hover fieldset": {
                                borderColor: "#67b3d9",
                            },
                            "&.Mui-focused fieldset": {
                                borderColor: "#67b3d9",
                            },
                        },
                        "& .MuiInputLabel-root": {
                            color: "#6cb3d9",
                        },
                        "& .MuiInputBase-input": {
                            color: "white",
                        }
                    }}
                />
                <Button
                    variant="contained"
                    endIcon={<SendIcon />}
                    onClick={handleSendMessage}
                    sx={{
                        backgroundColor: "#67b3d9",
                        textTransform: "none",
                        borderRadius: "10px",
                        padding: "8px 18px",
                        "&:hover": {
                            backgroundColor: "#5fa5c7"
                        },
                        "&:active": {
                            backgroundColor: "#4f92b5"
                        }
                    }}
                >
                    Send
                </Button>
            </div>
        </div>
    )
}