
import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { MapPin, Search, X } from "lucide-react-native";

type SearchResult = {
  place_id: number;
  display_name: string;
  lat: string;
  lon: string;
};

type Props = {
  onSelect: (latitude: number, longitude: number) => void;
  placeholder?: string;
};

export default function LocationSearch({
  onSelect,
  placeholder = "Search city or location...",
}: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (query.trim().length < 3 || !open) {
      setResults([]);
      setLoading(false);
      return;
    }

    const controller = new AbortController();

    const timeout = setTimeout(async () => {
      setLoading(true);
      setError(false);

      try {
        const url =
          "https://nominatim.openstreetmap.org/search" +
          `?q=${encodeURIComponent(query.trim())}` +
          "&format=json&limit=5&addressdetails=1";

        const response = await fetch(url, {
          signal: controller.signal,
          headers: {
            Accept: "application/json",
          },
        });

        if (!response.ok) throw new Error("Search failed");

        const data: SearchResult[] = await response.json();
        setResults(data);
      } catch (err) {
        if (!controller.signal.aborted) {
          setResults([]);
          setError(true);
        }
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }, 500);

    return () => {
      clearTimeout(timeout);
      controller.abort();
    };
  }, [query, open]);

  function selectLocation(item: SearchResult) {
    setQuery(item.display_name);
    setResults([]);
    setOpen(false);
    onSelect(Number(item.lat), Number(item.lon));
  }

  return (
    <View style={styles.wrapper}>
      <View style={styles.searchBar}>
        <Search size={20} color="#64748B" />

        <TextInput
          style={styles.input}
          placeholder={placeholder}
          placeholderTextColor="#94A3B8"
          value={query}
          onChangeText={(value) => {
            setQuery(value);
            setOpen(true);
          }}
          onFocus={() => setOpen(true)}
        />

        {loading ? (
          <ActivityIndicator color="#155BC7" />
        ) : query.length > 0 ? (
          <Pressable
            onPress={() => {
              setQuery("");
              setResults([]);
              setOpen(false);
            }}
          >
            <X size={19} color="#64748B" />
          </Pressable>
        ) : null}
      </View>

      {open && query.trim().length >= 3 && (
        <View style={styles.results}>
          {error ? (
            <Text style={styles.message}>
              Could not search locations.
            </Text>
          ) : !loading && results.length === 0 ? (
            <Text style={styles.message}>
              No locations found.
            </Text>
          ) : (
            <FlatList
              data={results}
              keyExtractor={(item) => String(item.place_id)}
              keyboardShouldPersistTaps="always"
              scrollEnabled={false}
              renderItem={({ item }) => (
                <Pressable
                  style={styles.resultItem}
                  onPress={() => selectLocation(item)}
                >
                  <MapPin size={18} color="#155BC7" />

                  <Text
                    style={styles.resultText}
                    numberOfLines={2}
                  >
                    {item.display_name}
                  </Text>
                </Pressable>
              )}
            />
          )}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    width: "100%",
    zIndex: 100,
  },
  searchBar: {
    height: 56,
    backgroundColor: "#FFFFFF",
    borderRadius: 16,
    paddingHorizontal: 16,
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    shadowColor: "#000000",
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 5,
  },
  input: {
    flex: 1,
    fontSize: 15,
    color: "#172033",
  },
  results: {
    marginTop: 6,
    backgroundColor: "#FFFFFF",
    borderRadius: 16,
    overflow: "hidden",
    elevation: 6,
    shadowColor: "#000000",
    shadowOpacity: 0.1,
    shadowRadius: 10,
    maxHeight: 300,
  },
  resultItem: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: "#E2E8F0",
  },
  resultText: {
    flex: 1,
    fontSize: 14,
    color: "#172033",
  },
  message: {
    padding: 16,
    color: "#64748B",
    fontSize: 14,
  },
});
