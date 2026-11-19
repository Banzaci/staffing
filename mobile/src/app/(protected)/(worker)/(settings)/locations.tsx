import { useEffect, useRef, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Pressable,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useRouter } from "expo-router";
import MapView, { Region } from "react-native-maps";
import * as Location from "expo-location";
import { ArrowLeft, Crosshair, MapPin } from "lucide-react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { updateWorkerLocation } from "@/api/workers/updateWorkerLocation";
import { useSession } from "@/hooks/useSession";

const BLUE = "#155BC7";

const DEFAULT_REGION: Region = {
  latitude: 10.3157,
  longitude: 123.8854,
  latitudeDelta: 0.08,
  longitudeDelta: 0.08,
};

type Coordinates = {
  latitude: number;
  longitude: number;
};

export default function LocationsScreen() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { data: session } = useSession();
  const mapRef = useRef<MapView>(null);

  const [region, setRegion] = useState<Region>(DEFAULT_REGION);
  const [loading, setLoading] = useState(false);
  const [selectedLocation, setSelectedLocation] =
    useState<Coordinates | null>(null);

  const latitude = session?.worker_profile?.latitude;
  const longitude = session?.worker_profile?.longitude;

  useEffect(() => {
    if (latitude == null || longitude == null) return;

    const savedRegion: Region = {
      latitude,
      longitude,
      latitudeDelta: 0.08,
      longitudeDelta: 0.08,
    };

    setRegion(savedRegion);
    setSelectedLocation({ latitude, longitude });

    mapRef.current?.animateToRegion(savedRegion, 500);
  }, [latitude, longitude]);

  async function useCurrentLocation() {
    setLoading(true);

    try {
      const permission =
        await Location.requestForegroundPermissionsAsync();

      if (permission.status !== "granted") {
        Alert.alert(
          "Location permission",
          "Please allow location access or choose a location manually."
        );
        return;
      }

      const position = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.Balanced,
      });

      const nextRegion: Region = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        latitudeDelta: 0.08,
        longitudeDelta: 0.08,
      };

      setRegion(nextRegion);
      setSelectedLocation({
        latitude: nextRegion.latitude,
        longitude: nextRegion.longitude,
      });

      mapRef.current?.animateToRegion(nextRegion, 500);
    } catch {
      Alert.alert("Error", "Unable to get your current location.");
    } finally {
      setLoading(false);
    }
  }

  const locationMutation = useMutation({
    mutationFn: updateWorkerLocation,
    onSuccess: async (data, variables) => {
      queryClient.setQueriesData(
        { queryKey: ["session"] },
        (old: typeof session) => {
          if (!old) return old;

          return {
            ...old,
            worker_profile: {
              ...old.worker_profile,
              latitude: variables.latitude,
              longitude: variables.longitude,
            },
          };
        }
      );

      await queryClient.invalidateQueries({
        queryKey: ["session"],
      });

      Alert.alert("Success", "Location saved successfully.");
      router.back();
    },
    onError: () => {
      Alert.alert("Error", "Could not save location.");
    },
  });

  function saveLocation() {
    if (!selectedLocation || locationMutation.isPending) return;

    locationMutation.mutate(selectedLocation);
  }

  return (
    <SafeAreaView style={styles.container} edges={["top", "bottom"]}>
      <View style={styles.header}>
        <Pressable onPress={() => router.back()} style={styles.back}>
          <ArrowLeft size={24} color="#101936" />
        </Pressable>

        <Text style={styles.heading}>My Location</Text>

        <View style={styles.headerSpacer} />
      </View>

      <Text style={styles.subtitle}>
        Move the map to choose where you want to find jobs.
      </Text>

      <View style={styles.mapContainer}>
        <MapView
          ref={mapRef}
          style={StyleSheet.absoluteFill}
          initialRegion={DEFAULT_REGION}
          showsUserLocation
          onRegionChangeComplete={(nextRegion) => {
            setRegion(nextRegion);
            setSelectedLocation({
              latitude: nextRegion.latitude,
              longitude: nextRegion.longitude,
            });
          }}
        />

        <View pointerEvents="none" style={styles.centerMarker}>
          <MapPin size={42} color={BLUE} fill="#FFFFFF" />
        </View>

        <Pressable
          style={styles.gpsButton}
          onPress={useCurrentLocation}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color={BLUE} />
          ) : (
            <Crosshair size={23} color={BLUE} />
          )}
        </Pressable>
      </View>

      <View style={styles.footer}>
        <Text style={styles.label}>Selected coordinates</Text>

        <Text style={styles.coordinates}>
          {region.latitude.toFixed(5)}, {region.longitude.toFixed(5)}
        </Text>

        <Pressable
          style={[
            styles.saveButton,
            locationMutation.isPending && styles.saveButtonDisabled,
          ]}
          onPress={saveLocation}
          disabled={!selectedLocation || locationMutation.isPending}
        >
          {locationMutation.isPending ? (
            <ActivityIndicator color="#FFFFFF" />
          ) : (
            <Text style={styles.saveText}>Save location</Text>
          )}
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#D9EFFF",
  },
  header: {
    height: 60,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 20,
  },
  back: {
    width: 40,
    height: 40,
    justifyContent: "center",
  },
  heading: {
    fontSize: 22,
    fontWeight: "800",
    color: "#101936",
  },
  headerSpacer: {
    width: 40,
  },
  subtitle: {
    fontSize: 14,
    color: "#34425B",
    textAlign: "center",
    paddingHorizontal: 25,
    marginBottom: 16,
  },
  mapContainer: {
    flex: 1,
    marginHorizontal: 16,
    borderRadius: 22,
    overflow: "hidden",
    backgroundColor: "#E5E7EB",
  },
  centerMarker: {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: [
      { translateX: -21 },
      { translateY: -42 },
    ],
  },
  gpsButton: {
    position: "absolute",
    right: 16,
    bottom: 20,
    width: 50,
    height: 50,
    borderRadius: 16,
    backgroundColor: "#FFFFFF",
    alignItems: "center",
    justifyContent: "center",
    elevation: 3,
  },
  footer: {
    padding: 20,
    gap: 10,
  },
  label: {
    fontSize: 13,
    color: "#64748B",
  },
  coordinates: {
    fontSize: 16,
    fontWeight: "700",
    color: "#101936",
  },
  saveButton: {
    height: 54,
    borderRadius: 16,
    backgroundColor: BLUE,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 8,
  },
  saveButtonDisabled: {
    opacity: 0.6,
  },
  saveText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
});