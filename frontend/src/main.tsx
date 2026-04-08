import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter } from "react-router-dom"
import { TooltipProvider } from "@/components/ui/tooltip"
import { Toaster } from "@/components/ui/sonner"
import App from "./App"
import "./index.css"

const root = document.getElementById("root")!

function Root() {
  const dark = JSON.parse(localStorage.getItem("novel-app-store") || "{}").state?.darkMode ?? true
  if (dark) document.documentElement.classList.add("dark")

  return (
    <StrictMode>
      <BrowserRouter>
        <TooltipProvider>
          <App />
          <Toaster richColors position="top-right" />
        </TooltipProvider>
      </BrowserRouter>
    </StrictMode>
  )
}

createRoot(root).render(<Root />)
