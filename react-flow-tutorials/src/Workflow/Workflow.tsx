import React, { useCallback, useState } from "react";
import ReactFlow, {
  addEdge,
  Background,
  Connection,
  Controls,
  useEdgesState,
  useNodesState,
} from "reactflow";
import "reactflow/dist/style.css";
import { Box, IconButton, Select, VStack } from "@chakra-ui/react";
import { GoSidebarCollapse } from "react-icons/go";
import { initialEdges, initialNodes } from "./Workflow.constants";
import PaymentInit from "./PaymentInit";
import PaymentCountry from "./PaymentCountry";
import PaymentProvider from "./PaymentProvider";
import PaymentProviderSelect from "./PaymentProviderSelect";
import CustomEdge from "./CustomEdge";

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
  const [selectedSentiment, setSelectedSentiment] = useState("all");
  const [isSidebarOpen, setSidebarOpen] = useState(true);

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

  const handleSentimentChange = (event: any) => {
    setSelectedSentiment(event.target.value);
    // You can implement filtering here
  };

  return (
    <Box display="flex" height="100vh" width="100vw">
      {/* Sidebar */}
      <Box
        width={isSidebarOpen ? "250px" : "20px"}
        transition="width 0.3s"
        bg="gray.50"
        borderRight="1px solid"
        borderColor="gray.200"
        position="relative"
        overflow="hidden"
      >
        {isSidebarOpen && (
          <VStack align="stretch" spacing="4" p="3">
            <Select
              placeholder="Select Sentiment"
              onChange={handleSentimentChange}
              value={selectedSentiment}
            >
              <option value="positive">Positive</option>
              <option value="neutral">Neutral</option>
              <option value="negative">Negative</option>
              <option value="all">All</option>
            </Select>
          </VStack>
        )}

        <IconButton
          icon={<GoSidebarCollapse />}
          aria-label="Toggle Sidebar"
          size="sm"
          onClick={toggleSidebar}
          position="absolute"
          top="2%"
          right="-12px"
          transform={isSidebarOpen ? "rotate(0deg)" : "rotate(180deg)"}
          borderRadius="full"
          zIndex={10}
          bg="white"
          boxShadow="md"
        />
      </Box>

      {/* React Flow Canvas */}
      <Box flex="1" position="relative">
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
  );
};
