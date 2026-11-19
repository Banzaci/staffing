import { View, Text } from "react-native";

export default function Screen() {
  return (
    <View
      style={{
        flex: 1,
        backgroundColor: "#F8FAFC",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text style={{ fontSize: 24, color: "#155BC7" }}>
        Home
      </Text>
    </View>
  );
}