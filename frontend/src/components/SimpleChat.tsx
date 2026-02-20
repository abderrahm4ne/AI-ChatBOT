import { useState, type ChangeEvent } from 'react'

export default function SimpleChat(){
    const [input, setInput] = useState<string>("")
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [completion, setCompletion] = useState<string>("")
    const [file, setFile] = useState<File | null>(null)
    const [isUploaded, setIsUploaded] = useState<boolean>(false)

    const handleFileUpload = async () => {
        if(!file) return
        setIsLoading(true)

        try{
            const response = await fetch('http://localhost:8000/upload-pdf', {
                method: "POST",
                body: file
            })

            if(response.ok){
                setIsUploaded(true)
                alert('file uploaded successfully !')
            }
        }
        catch (error){
            console.error("Upload file error ", error)
        }
        finally{
            setIsLoading(false)
        }
    } 
 
    const handleSubmit = async (e: ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        setIsLoading(true);
        setCompletion("");
        
        try{
            const response = await fetch("http://localhost:8000/chat", {
                method: "POST",
                body: JSON.stringify({
                    thread_id: "test-session",
                    prompt: input
                })
            })

            if(!response)
                return

            const reader = response.body?.getReader()
            const decoder = new TextDecoder();

            while(true){
                const { value, done } = await reader?.read()
                if (done) break

                const chunk = decoder.decode(value, { stream: true });
                setCompletion(prev => prev + chunk)
            }
        }
        catch(error){
            console.error("error occured", error)
        }
        finally{
            setIsLoading(false)
        }
    }


    return(
    <div className="p-8 max-w-2xl mx-auto space-y-4">
        <h1 className="text-xl font-bold">FastAPI Agent Tester</h1>
        <div className="flex items-center gap-4 p-4 border rounded bg-blue-50">
            <input
                className="flex-1 p-2 border rounded shadow-sm"
                type='file'
                accept='.pdf'
                onChange={
                    (e: ChangeEvent<HTMLInputElement>) => {
                            if(e.target.files){
                                setFile(e.target.files[0])
                            }
                        }}
                />
            <button 
            onClick={handleFileUpload}
            className="bg-blue-600 text-white px-4 py-1 rounded disabled:bg-gray-400 hover:cursor-pointer"
            disabled={!file || isLoading || isUploaded}>
                {isUploaded? 'Uploaded' : 'Upload PDF'}
            </button>
        </div>
        
        <form onSubmit={handleSubmit} className="flex gap-2">
            <input
                className="flex-1 p-2 border rounded shadow-sm"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about the PDF..."
            />
            <button 
            type="submit" 
            className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 disabled:bg-gray-400"
            disabled={isLoading}
            >
            {isLoading ? "Thinking..." : "Send"}
            </button>
        </form>
        
        <div className="p-4 border rounded-lg bg-gray-50 min-h-70 whitespace-pre-wrap">
            {completion || (isLoading ? "..." : "Agent response will appear here...")}
        </div>
    </div>
    )
}