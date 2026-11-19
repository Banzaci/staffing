
import { useEffect } from "react";
import { Tabs } from "expo-router";
import {
  House,
  Search,
  CalendarDays,
  UserRound,
  Settings,
} from "lucide-react-native";
import { View, StyleSheet } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withTiming,
} from "react-native-reanimated";

import {
  useWorkerTabBar,
  WorkerTabBarProvider,
} from "@/contexts/WorkerTabBarContext";
import { BottomTabBar, BottomTabBarProps } from "expo-router/build/layouts/TabsClient.js";

const COLORS = {
  home: "#155BC7",
  jobs: "#10B981",
  shifts: "#F59E0B",
  profile: "#A855F7",
  settings: "#EC4899",
};

function AnimatedTabBar(props: BottomTabBarProps) {
  const { minimized } = useWorkerTabBar();
  const translateY = useSharedValue(0);

  useEffect(() => {
    translateY.value = withTiming(minimized ? 36 : 0, {
      duration: 300,
    });
  }, [minimized, translateY]);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateY: translateY.value }],
  }));

  return (
    <Animated.View
      pointerEvents={minimized ? "none" : "auto"}
      style={[styles.tabBarWrapper, animatedStyle]}
    >
      <BottomTabBar {...props} />
    </Animated.View>
  );
}

function WorkerTabsContent() {
  return (
    <Tabs
      tabBar={(props) => <AnimatedTabBar {...props} />}
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: "#172033",
        tabBarInactiveTintColor: "#64748B",
        tabBarLabelStyle: {
          fontSize: 11,
          fontWeight: "600",
          marginTop: 4,
        },
        tabBarStyle: {
          backgroundColor: "#FFFFFF",
          borderTopWidth: 0,
          borderRadius: 24,
          height: 72,
          paddingTop: 10,
          paddingBottom: 8,
          shadowColor: "#000000",
          shadowOffset: { width: 0, height: 4 },
          shadowOpacity: 0.1,
          shadowRadius: 12,
          elevation: 8,
        },
        tabBarItemStyle: {
          borderRadius: 16,
        },
        tabBarIconStyle: {
          marginTop: 2,
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Home",
          tabBarIcon: ({ focused }) => (
            <View style={focused ? styles.activeIcon : undefined}>
              <House
                size={23}
                color={COLORS.home}
                strokeWidth={focused ? 2.8 : 2}
              />
            </View>
          ),
        }}
      />
      <Tabs.Screen
        name="jobs"
        options={{
          title: "Jobs",
          tabBarIcon: ({ focused }) => (
            <View style={focused ? styles.activeIcon : undefined}>
              <Search
                size={23}
                color={COLORS.jobs}
                strokeWidth={focused ? 2.8 : 2}
              />
            </View>
          ),
        }}
      />
      <Tabs.Screen
        name="shifts"
        options={{
          title: "My Shifts",
          tabBarIcon: ({ focused }) => (
            <View style={focused ? styles.activeIcon : undefined}>
              <CalendarDays
                size={23}
                color={COLORS.shifts}
                strokeWidth={focused ? 2.8 : 2}
              />
            </View>
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: "Profile",
          tabBarIcon: ({ focused }) => (
            <View style={focused ? styles.activeIcon : undefined}>
              <UserRound
                size={23}
                color={COLORS.profile}
                strokeWidth={focused ? 2.8 : 2}
              />
            </View>
          ),
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: "Settings",
          tabBarIcon: ({ focused }) => (
            <View style={focused ? styles.activeIcon : undefined}>
              <Settings
                size={23}
                color={COLORS.settings}
                strokeWidth={focused ? 2.8 : 2}
              />
            </View>
          ),
        }}
      />
    </Tabs>
  );
}

export default function WorkerTabsLayout() {
  return (
    <WorkerTabBarProvider>
      <WorkerTabsContent />
    </WorkerTabBarProvider>
  );
}

const styles = StyleSheet.create({
  tabBarWrapper: {
    position: "absolute",
    bottom: 12,
    left: 14,
    right: 14,
    zIndex: 10,
  },
  activeIcon: {
    backgroundColor: "#F0F6FF",
    borderRadius: 12,
    padding: 6,
    marginTop: -6,
  },
});
