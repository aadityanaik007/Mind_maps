import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ChakraProvider } from "@chakra-ui/react";
import Homepage from "./Homepage/Homepage";
import { Workflow } from "./Workflow/Workflow"; // your mindmap page

function App() {
  return (
    <ChakraProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/mindmap" element={<Workflow />} />
        </Routes>
      </Router>
    </ChakraProvider>
  );
}

export default App;
