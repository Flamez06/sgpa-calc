import FileUploader from "./components/FileUploader"
async function testBackend() {
  const response = await fetch("http://127.0.0.1:8000/hello")
  const data = await response.json()
  console.log(data)
}
function App() {
  testBackend()
  return (
        <>
          <div className="App">
              <h1>My App</h1>
              <FileUploader />
          </div>
        </>
  )
}

export default App
