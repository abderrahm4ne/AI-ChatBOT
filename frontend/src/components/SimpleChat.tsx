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

const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

    const threadID = useMemo(() => (uuidv4()), []);

    const [message, setMessage] = useState<string>('')
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [isFileLoading, setIsFileLoading] = useState<boolean>(false)
    const [chatHistory, setChatHistory] = useState<Message[]>([]);

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0]
        if(!selectedFile) return
        
        const formData = new FormData()
        formData.append("file", selectedFile)
        setIsFileLoading(true)
        try{
            await fetch('http://localhost:8000/upload-pdf', {
                method: 'POST',
                body: formData
            })
            alert("PDF has been sent to the agent")
        }
        catch(error){
            console.error("Error Occured", error)
        }
        finally{
            setIsFileLoading(false)
        }
    }

    const handleSendMessage = async () => {

        if (!message.trim()) return alert("Enter a question")

        const userPrompt: Message = {
            role: "user",
            content: message
        }

        setChatHistory(prev => [
            ...prev,
            userPrompt,
            { role: "ai", content: "" }
        ])
        
        setMessage("")
        setIsLoading(true)

        let finalText = ''

        try {
            const response = await fetch("http://localhost:8000/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    prompt: message,
                    thread_id: threadID
                })
            })
            const reader = response.body?.getReader()
            const decoder = new TextDecoder();

            if (!reader) return

            while(true){
                const { value, done } = await reader.read()
                if(done) break

                const chunk = decoder.decode(value, { stream: true })

                // console.log("New chunk from AI", chunk)
                const lines = chunk.split("\n")
                // console.log(lines)
                for (const line of lines) {
                    // console.log(line)
                    if (!line.trim()) continue;

                    const text = line.replace("data:", "");
                    if (!text) continue

                    finalText += text 
                    setChatHistory(prev => {
                        const newChat = [...prev]
                        const last = newChat.length - 1

                        if(newChat[last]?.role === 'ai') {
                            newChat[last].content = finalText
                        }
                        return newChat
                    })
                }
                await delay(100);
            }

        } catch (error) {
            console.error("Error sending message", error)
        }
        finally{
            setIsLoading(false)
        }
    }

    return(
        <div className="p-2 px-4 mx-auto space-y-4 bg-slate-800 flex flex-col rounded-xl w-150">

            <div className='flex flex-col gap-0.2'>
                <h3 className='font-bold text-blue-300 '>RAG AI ChatBOT</h3>
                <p className='text-sm text-gray-400'>Thread id : {threadID}</p>
            </div>

            <div className='flex flex-col'>

                <Button
                    component="label"
                    role={undefined}
                    variant="contained"
                    startIcon={isFileLoading ? <CircularProgress size={20} color="inherit" /> : <CloudUploadIcon />}
                    disabled={isFileLoading}
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

            <div className='border border-[#67b3d9] rounded-md p-4 h-110 overflow-y-auto bg-slate-900 text-white flex flex-col gap-3'>
                {chatHistory.map((msg, i) => (
                    <div
                        key={i}
                        className={`flex items-start gap-2 ${
                        msg.role === "user" ? "justify-end" : "justify-start"
                        }`}
                    >
                        {msg.role === "ai" && (
                        <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-sm font-bold">
                            AI
                        </div>
                        )}

                        <div
                        className={`p-2 rounded-lg max-w-[70%] ${
                            msg.role === "user"
                            ? "bg-blue-600 text-white"
                            : "bg-slate-700 text-white"
                        }`}
                        >
                        {msg.content}
                        </div>
                    </div>
                    ))}
            </div>

            <div className='flex flex-col gap-1'>
                <TextField
                    label="Write your question here.."
                    onChange={(e) => setMessage(e.target.value)}
                    multiline
                    value={message}
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
                    disabled={isLoading}
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