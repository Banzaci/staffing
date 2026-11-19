
import { useEffect, useMemo, useRef, useState } from "react";
import {
  Pressable,
  Modal,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useQuery } from "@tanstack/react-query";
import MapView, { Marker, Region } from "react-native-maps";
import BottomSheet, {
  BottomSheetView,
} from "@gorhom/bottom-sheet";
import LocationSearch from "@/components/maps/LocationSearch";
import { BriefcaseBusiness, X } from "lucide-react-native";
import { useRouter } from "expo-router";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { useSession } from "@/hooks/useSession";
import { useLanguage } from "@/providers/LanguageProvider";
import DashboardActionCard from "@/components/dashboard/DashboardActionCard";
import { api } from "@/libs/api";
import { NearbyJob } from "@/app/types/job-shifts";
import ApplyForShiftButton from "@/components/jobs/ApplyForShiftButton";
import { useWorkerTabBar } from "@/contexts/WorkerTabBarContext";

const WORKER_COLOR = "#155BC7";

export default function WorkerIndex() {
  const { data: session, isPending } = useSession();
  const { setMinimized } = useWorkerTabBar();
  const { t } = useLanguage();
  const router = useRouter();
  const insets = useSafeAreaInsets();

  const mapRef = useRef<MapView>(null);
  const sheetRef = useRef<BottomSheet>(null);

  const [showLocationModal, setShowLocationModal] = useState(false);
  const [selectedJob, setSelectedJob] = useState<NearbyJob | null>(null);

  const latitude = session?.worker_profile?.latitude;
  const longitude = session?.worker_profile?.longitude;

  const [mapCenter, setMapCenter] = useState<{
    latitude: number;
    longitude: number;
  } | null>(null);

  const searchLatitude = mapCenter?.latitude ?? latitude;
  const searchLongitude = mapCenter?.longitude ?? longitude;

  const snapPoints = useMemo(() => ["35%", "75%"], []);

  const { data: jobs = [] } = useQuery<NearbyJob[]>({
    queryKey: ["nearby-jobs", searchLatitude, searchLongitude],
    queryFn: () =>
      api<NearbyJob[]>(
        `/api/private/v1/job-shifts/nearby?latitude=${searchLatitude}&longitude=${searchLongitude}`
      ),
    enabled: searchLatitude != null && searchLongitude != null,
  });

  useEffect(() => {
    if (isPending || !session) return;
    setShowLocationModal(latitude == null || longitude == null);
  }, [isPending, session, latitude, longitude]);

  const openJob = (job: NearbyJob) => {
    setSelectedJob(job);
    setMinimized(true);
    sheetRef.current?.snapToIndex(0);

    mapRef.current?.animateToRegion(
      {
        latitude: job.latitude,
        longitude: job.longitude,
        latitudeDelta: 0.08,
        longitudeDelta: 0.08,
      },
      350
    );
  };

  if (isPending || !session) return null;

  const hasSkills = session.skills.length > 0;

  const region: Region | null =
    latitude != null && longitude != null
      ? {
          latitude,
          longitude,
          latitudeDelta: 0.08,
          longitudeDelta: 0.08,
        }
      : null;

  return (
    <View style={styles.container}>
      {region ? (
        <MapView
          ref={mapRef}
          style={styles.map}
          initialRegion={region}
          zoomEnabled
          scrollEnabled
          onRegionChangeComplete={(newRegion) => {
            setMapCenter({
              latitude: newRegion.latitude,
              longitude: newRegion.longitude,
            });
          }}
        >
          {latitude != null && longitude != null && (
            <Marker
              coordinate={{ latitude, longitude }}
              title="Your location"
              pinColor={WORKER_COLOR}
            />
          )}

          {jobs.map((job) => (
            <Marker
              key={job.id}
              coordinate={{
                latitude: job.latitude,
                longitude: job.longitude,
              }}
              pinColor={
                selectedJob?.id === job.id
                  ? "#DC2626"
                  : "#F59E0B"
              }
              onPress={() => openJob(job)}
            />
          ))}
        </MapView>
      ) : (
        <View style={styles.placeholder}>
          <Text style={styles.placeholderText}>
            Set your location in Settings to see nearby jobs.
          </Text>
        </View>
      )}

      <View
        pointerEvents="box-none"
        style={[styles.overlay, { top: insets.top + 16 }]}
      >
        <View style={styles.mapHeader}>
          <View style={styles.searchContainer}>
            <LocationSearch
              onSelect={(latitude, longitude) => {
                setMapCenter({ latitude, longitude });

                mapRef.current?.animateToRegion(
                  {
                    latitude,
                    longitude,
                    latitudeDelta: 0.08,
                    longitudeDelta: 0.08,
                  },
                  600
                );
              }}
            />
          </View>
        </View>
        {!hasSkills && (
          <DashboardActionCard
            title={t.addSkills}
            description={t.addSkillsDescription}
            icon={BriefcaseBusiness}
            color={WORKER_COLOR}
            onPress={() => {}}
          />
        )}
      </View>
      {selectedJob && (
        <BottomSheet
          ref={sheetRef}
          index={0}
          snapPoints={snapPoints}
          enablePanDownToClose
          onClose={() => {
            setSelectedJob(null);
            setMinimized(false);
          }}
          handleIndicatorStyle={styles.sheetHandle}
          backgroundStyle={styles.sheetBackground}
        >
          <BottomSheetView style={styles.sheetContent}>
            <View style={styles.sheetTitleRow}>
              <View style={styles.sheetTitleContent}>
                <Text style={styles.jobType}>
                  {selectedJob.job_type}
                </Text>

                <Text style={styles.businessName}>
                  {selectedJob.business_name}
                </Text>
              </View>
              <Pressable
                style={styles.closeButton}
                onPress={() => sheetRef.current?.close()}
              >
                <X size={21} color="#475569" />
              </Pressable>
            </View>
            <Text style={styles.jobRate}>
              {selectedJob.hourly_rate}{" "}
              {selectedJob.currency}/hour
            </Text>
            <Text style={styles.jobDistance}>
              {selectedJob.distance_km} km away
            </Text>
            <Text style={styles.jobDescription}>
              {selectedJob.description ||
                "No description available."}
            </Text>
            <ApplyForShiftButton shiftId={selectedJob.id} />
          </BottomSheetView>
        </BottomSheet>
      )}
      <Modal
        visible={showLocationModal}
        transparent
        animationType="fade"
        onRequestClose={() => setShowLocationModal(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>
              Set your location
            </Text>

            <Text style={styles.modalDescription}>
              Please set your location to find jobs near you.
            </Text>

            <Pressable
              style={styles.locationButton}
              onPress={() => {
                setShowLocationModal(false);
                router.push(
                  "/(protected)/(worker)/(settings)/locations"
                );
              }}
            >
              <Text style={styles.locationButtonText}>
                Set my location
              </Text>
            </Pressable>

            <Pressable
              onPress={() => setShowLocationModal(false)}
            >
              <Text style={styles.laterText}>
                Maybe later
              </Text>
            </Pressable>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F5F9FF",
  },
  map: {
    flex: 1,
  },
  overlay: {
    position: "absolute",
    left: 20,
    right: 20,
    gap: 14,
    zIndex: 2,
  },
  mapHeader: {
    backgroundColor: "#FFFFFF",
    borderRadius: 18,
    paddingHorizontal: 18,
    paddingVertical: 16,
    flexDirection: "row",
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 4,
  },
  searchContainer: {
    flex: 1,
  },
  placeholder: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 20,
  },
  placeholderText: {
    fontSize: 14,
    color: "#64748B",
    textAlign: "center",
  },
  sheetBackground: {
    backgroundColor: "#FFFFFF",
    borderTopLeftRadius: 28,
    borderTopRightRadius: 28,
  },
  sheetHandle: {
    width: 42,
    height: 5,
    backgroundColor: "#CBD5E1",
  },
  sheetContent: {
    paddingHorizontal: 24,
    paddingTop: 12,
    paddingBottom: 110,
    gap: 12,
  },
  sheetTitleRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
  },
  sheetTitleContent: {
    flex: 1,
  },
  jobType: {
    fontSize: 25,
    fontWeight: "700",
    color: "#172033",
    textTransform: "capitalize",
  },
  businessName: {
    fontSize: 16,
    color: "#64748B",
    marginTop: 5,
  },
  closeButton: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: "#F1F5F9",
    alignItems: "center",
    justifyContent: "center",
  },
  jobRate: {
    fontSize: 19,
    fontWeight: "700",
    color: WORKER_COLOR,
  },
  jobDistance: {
    fontSize: 14,
    color: "#64748B",
  },
  jobDescription: {
    fontSize: 15,
    color: "#475569",
    lineHeight: 23,
  },
  viewJobButton: {
    backgroundColor: WORKER_COLOR,
    paddingVertical: 16,
    borderRadius: 14,
    alignItems: "center",
    marginTop: 8,
  },
  viewJobText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.4)",
    justifyContent: "center",
    padding: 24,
  },
  modalContent: {
    backgroundColor: "#FFFFFF",
    borderRadius: 22,
    padding: 28,
    alignItems: "center",
  },
  modalTitle: {
    fontSize: 22,
    fontWeight: "700",
    color: "#172033",
  },
  modalDescription: {
    fontSize: 15,
    color: "#64748B",
    textAlign: "center",
    marginTop: 12,
    marginBottom: 24,
  },
  locationButton: {
    backgroundColor: WORKER_COLOR,
    borderRadius: 14,
    paddingVertical: 16,
    width: "100%",
    alignItems: "center",
  },
  locationButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
  laterText: {
    color: "#64748B",
    marginTop: 20,
    fontSize: 14,
  },
});
