import { Box, Button, Heading, Text, VStack, Image } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/logo.jpg";
const Homepage = () => {
  const navigate = useNavigate();

  return (
    <Box
      height="100vh"
      bg="gray.50"
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
    >
      <Box mb={6}>
        <Image src={logo} alt="FinMap Logo" maxH="300px" mx="auto" />
      </Box>

      <VStack spacing={6}>
        <Heading size="xl">Welcome to FinMap</Heading>
        <Text fontSize="md">
          Explore financial data visually and interactively.
        </Text>
        <Button
          colorScheme="teal"
          size="lg"
          onClick={() => navigate("/mindmap")}
        >
          Go to MindMap Playground
        </Button>
      </VStack>
    </Box>
  );
};

export default Homepage;
