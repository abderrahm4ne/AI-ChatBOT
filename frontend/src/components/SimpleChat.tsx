import { v4 as uuidv4 } from 'uuid'


export default function SimpleChat(){

    const threadID = uuidv4();



    return(
        <div className="p-2 px-4 max-w-2xl mx-auto space-y-4 bg-slate-800 flex flex-col rounded-xl min-w-100">

            <div className='flex flex-col gap-0.2'>
                <h3 className='font-bold text-blue-300 '>RAG AI ChatBOT</h3>
                <p className='text-sm text-gray-400'>Thread id : {threadID}</p>
            </div>

            <div className='flex flex-col gap-1'>

                <input
                    type="file"
                    className="hidden"
                    onChange={}
                />

                <input type="button" className='border-1 border-cyan-700 p-0.5 rounded-sm text-white hover:cursor-pointer' value={"Upload PDF"}/>

            </div>

            <main className='bg-slate-800 px-1 py-2 text-md rounded-sm'>
                sd
            </main>
        </div>
    )
}