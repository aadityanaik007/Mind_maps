import { Box, Text, VStack, Image, Button } from "@chakra-ui/react";
import logo from "../assets/logo.jpg"; // Adjust the path to your logo image
const Sidebar = ({ items }: { items: string[] }) => {
  return (
    <Box
      height="100vh"
      width="100%"
      bg="white"
      p={4}
      display="flex"
      flexDirection="column"
      alignItems="center"
    >
      {/* Logo Section */}
      <Box mb={6} textAlign="center">
        <Image src={logo} alt="FinMap Logo" maxH="50px" mx="auto" mb={2} />
        <Text fontWeight="bold" fontSize="lg">
          FinMap
        </Text>
      </Box>

      {/* Dynamic Buttons */}
      <VStack spacing={4} width="100%">
        {items.map((item, index) => (
          <Button
            key={index}
            width="100%"
            justifyContent="flex-start"
            variant="ghost"
            fontWeight="bold"
          >
            {item}
          </Button>
        ))}
      </VStack>
    </Box>
  );
};

export default Sidebar;
