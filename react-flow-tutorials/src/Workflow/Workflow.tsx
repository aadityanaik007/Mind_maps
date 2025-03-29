import React, { useCallback, useEffect, useState } from "react";
import ReactFlow, {
  addEdge,
  Background,
  Connection,
  Controls,
  useEdgesState,
  useNodesState,
} from "reactflow";
import "reactflow/dist/style.css";
import { Box, IconButton } from "@chakra-ui/react";
import { GoSidebarCollapse } from "react-icons/go";
import axios from "axios";
import { initialEdges, initialNodes } from "./Workflow.constants";
import PaymentInit from "./PaymentInit";
import PaymentCountry from "./PaymentCountry";
import PaymentProvider from "./PaymentProvider";
import PaymentProviderSelect from "./PaymentProviderSelect";
import CustomEdge from "./CustomEdge";
import Sidebar from "../Sidebar/Sidebar";

const nodeTypes = {
  paymentInit: PaymentInit,
  paymentCountry: PaymentCountry,
  paymentProvider: PaymentProvider,
  paymentProviderSelect: PaymentProviderSelect,
};

const edgeTypes = {
  customEdge: CustomEdge,
};

export const Workflow = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [tickers, setTickers] = useState<string[]>([]);
  const [selectedTicker, setSelectedTicker] = useState("AAPL");
  const [sidebarItems, setSidebarItems] = useState<string[]>([]);

  const toggleSidebar = () => setSidebarOpen(!isSidebarOpen);

  const onConnect = useCallback(
    (connection: Connection) => {
      const edge = {
        ...connection,
        animated: true,
        id: `${edges.length + 1}`,
        type: "customEdge",
      };
      setEdges((prevEdges) => addEdge(edge, prevEdges));
    },
    [edges]
  );

  useEffect(() => {
    const fetchTickers = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/get_all_tickers"
        );
        setTickers(response.data);
      } catch (error) {
        console.error("Failed to fetch tickers:", error);
      }
    };

    const fetchSidebarItems = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/sidebar_data");
        setSidebarItems(response.data);
      } catch (error) {
        console.error("Failed to fetch sidebar items:", error);
      }
    };

    fetchTickers();
    fetchSidebarItems();
  }, []);

  return (
    <Box display="flex" height="100vh" width="100vw" position="relative">
      {/* Sidebar */}
      <Box
        width={isSidebarOpen ? "250px" : "0"}
        transition="width 0.3s"
        bg="gray.50"
        borderRight="1px solid"
        borderColor="gray.200"
        overflow="hidden"
      >
        {isSidebarOpen && <Sidebar items={sidebarItems} />}
      </Box>

      {/* Collapser Button */}
      <IconButton
        icon={<GoSidebarCollapse />}
        aria-label="Toggle Sidebar"
        size="sm"
        onClick={toggleSidebar}
        position="absolute"
        top="3%"
        left={isSidebarOpen ? "250px" : "8px"}
        transform={isSidebarOpen ? "rotate(180deg)" : "rotate(0deg)"}
        borderRadius="full"
        zIndex={20}
        bg="white"
        boxShadow="md"
        transition="left 0.3s, transform 0.3s"
      />

      {/* Playground */}
      <Box flex="1" position="relative">
        {/* Top Bar */}
        <Box
          bg="white"
          p={4}
          borderBottom="1px solid"
          borderColor="gray.200"
          display="flex"
          alignItems="center"
          gap={4}
          zIndex={10}
          position="absolute"
          top="0"
          width="100%"
        >
          <select
            value={selectedTicker}
            onChange={(e) => setSelectedTicker(e.target.value)}
            style={{
              padding: "8px",
              borderRadius: "4px",
              marginLeft: "28px",
              border: "1px solid #ccc",
            }}
          >
            {tickers.map((ticker) => (
              <option key={ticker} value={ticker}>
                {ticker}
              </option>
            ))}
          </select>

          <Box bg="gray.100" px={4} py={2} borderRadius="md">
            📈 1Y Performance: +14.2%
          </Box>
          <Box bg="gray.100" px={4} py={2} borderRadius="md">
            📰 News: 124
          </Box>
          <Box bg="gray.100" px={4} py={2} borderRadius="md">
            🧾 M&A Events: 3
          </Box>
        </Box>

        {/* Canvas */}
        <Box height="100%" pt="64px">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            edgeTypes={edgeTypes}
            fitView
          >
            <Background />
            <Controls />
          </ReactFlow>
        </Box>
      </Box>
    </Box>
  );
};
