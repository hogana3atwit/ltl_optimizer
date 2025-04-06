import { useState, useEffect } from "react"
import { Card, CardContent } from "./components/ui/card"
import { Input } from "./components/ui/input"
import { Button } from "./components/ui/button"

export default function Dashboard() {
  const [weight, setWeight] = useState(1000)
  const [cube, setCube] = useState(10)
  const [origin, setOrigin] = useState("BOS")
  const [destination, setDestination] = useState("LAX")
  const [routeResult, setRouteResult] = useState(null)
  const [routeError, setRouteError] = useState("")
  const [serviceCenters, setServiceCenters] = useState([])

  useEffect(() => {
    fetch("/data/service_centers.csv")
      .then((res) => res.text())
      .then((text) => {
        const rows = text.trim().split("\n").slice(1)
        const centers = rows.map(row => row.split(",")[0])
        setServiceCenters(centers)
      })
      .catch(err => console.error("Failed to load service centers:", err))
  }, [])

  const routeShipment = async () => {
    setRouteError("")
    try {
      const res = await fetch("http://localhost:8000/route_shipment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ origin, destination, weight, cube })
      })
      if (!res.ok) throw new Error("Failed to fetch")
      const data = await res.json()
      setRouteResult(data)
    } catch (err) {
      console.error("Routing error:", err)
      setRouteError("Failed to calculate route. Check server.")
    }
  }

  return (
    <div className="p-6 grid gap-6 max-w-3xl mx-auto text-gray-800">
      {/* Disclaimer */}
      <Card>
        <CardContent className="p-4">
          <p className="text-sm text-gray-600 italic">
            ⚠️ Note: Mileage estimates are based on randomly generated distances and do not reflect actual driving distances.
          </p>
        </CardContent>
      </Card>

      {/* Service Centers */}
      <Card>
        <CardContent className="p-4">
          <h2 className="text-xl font-semibold mb-2">📍 Valid Service Centers</h2>
          <p className="text-sm text-gray-700">{serviceCenters.join(", ")}</p>
        </CardContent>
      </Card>

      {/* Shipment Input Form */}
      <Card>
        <CardContent className="p-4">
          <h2 className="text-xl font-semibold mb-4">📦 Route New Shipment</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Origin</label>
              <Input value={origin} onChange={(e) => setOrigin(e.target.value)} placeholder="e.g., BOS" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Destination</label>
              <Input value={destination} onChange={(e) => setDestination(e.target.value)} placeholder="e.g., LAX" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Weight (lbs)</label>
              <Input
                type="number"
                value={weight}
                onChange={(e) => setWeight(Number(e.target.value))}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Cube</label>
              <Input
                type="number"
                value={cube}
                onChange={(e) => setCube(Number(e.target.value))}
              />
            </div>
          </div>
          <Button className="mt-4" onClick={routeShipment}>Calculate Route</Button>
          {routeError && <p className="text-red-600 mt-2">{routeError}</p>}
        </CardContent>
      </Card>

      {/* Route Results */}
      {routeResult && (
        <Card>
          <CardContent className="p-4">
            <h2 className="text-xl font-semibold mb-4">🛣️ Route Summary</h2>
            <p><strong>Original Route:</strong> {routeResult.original_route.join(" → ")}</p>
            <p><strong>Final Route:</strong> {routeResult.final_route.join(" → ")}</p>
            <p><strong>Estimated Distance:</strong> {routeResult.estimated_distance} miles</p>
            {routeResult.bypass_details && routeResult.bypass_details.length > 0 ? (
              <div className="mt-4">
                <p><strong>Bypassed Centers:</strong> {routeResult.bypassed_centers.join(", ")}</p>
                <h3 className="text-lg font-semibold mb-2">🔍 Bypass Details</h3>
                {routeResult.bypass_details.map((b, index) => (
                  <div key={index} className="mb-3">
                    <p><strong>Center:</strong> {b.center}</p>
                    <p><strong>Combined Cube:</strong> {b.combined_cube}</p>
                    <p className="text-sm text-gray-700">Matching Shipments:</p>
                    <ul className="list-disc list-inside text-sm">
                      {b.matching_shipments.map((s, i) => (
                        <li key={i}>Destination: {s.destination}, Weight: {s.weight}, Cube: {s.cube}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            ) : (
              <p className="mt-4 text-sm text-gray-600 italic">No valid bypass was possible. Shipment followed the original route.</p>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  )
}

