import {useState} from "react"
function FileUploader() {
    const [file, setFile] = useState(null)
    const [status, setStatus] = useState("idle")
    
    function handleFileChange(event) {
        setFile(event.target.files[0])
    }

    async function handleFileUpload() {
        if (!file) return
        setStatus("uploading")
        const data=new FormData()
        data.append("file", file)
        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: data
        })
        const result = await response.json()
        console.log(result)
        setStatus("success")
    }

    return (
    <div>
        {file && <p>Selected file: {file.name}</p>}
        <input type="file" onChange={handleFileChange} />
        {status==="success" && <p className="text-green-500">File uploaded successfully!</p>}
        {file && status!="uploading" && <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={handleFileUpload}>upload</button>}
    </div>
    )
}   
export default FileUploader