'use client'

import { useEffect } from 'react'
import L from 'leaflet'
import { MapContainer, Marker, Popup, TileLayer, useMap } from 'react-leaflet'
import Link from 'next/link'
import type { School } from '@/lib/data'
import 'leaflet/dist/leaflet.css'

function makeIcon(active: boolean) {
  const color = active ? 'oklch(0.72 0.17 158)' : 'oklch(0.54 0.21 264)'
  return L.divIcon({
    className: 'academymap-pin',
    html: `
      <span style="
        display:flex;align-items:center;justify-content:center;
        width:34px;height:34px;border-radius:50% 50% 50% 0;
        transform:rotate(-45deg);
        background:${color};
        box-shadow:0 6px 16px -4px rgba(20,20,60,.5);
        border:2.5px solid white;">
        <span style="width:10px;height:10px;border-radius:50%;background:white;transform:rotate(45deg)"></span>
      </span>`,
    iconSize: [34, 34],
    iconAnchor: [17, 34],
    popupAnchor: [0, -32],
  })
}

function FitBounds({ schools, zoom }: { schools: School[]; zoom?: number }) {
  const map = useMap()
  useEffect(() => {
    if (schools.length === 1) {
      map.setView([schools[0].lat, schools[0].lng], zoom ?? 12)
    } else if (schools.length > 1) {
      const bounds = L.latLngBounds(schools.map((s) => [s.lat, s.lng]))
      map.fitBounds(bounds, { padding: [50, 50] })
    }
  }, [map, schools, zoom])
  return null
}

export default function LeafletMap({
  schools,
  activeId,
  zoom,
}: {
  schools: School[]
  activeId?: string
  zoom?: number
}) {
  const center: [number, number] = schools.length
    ? [schools[0].lat, schools[0].lng]
    : [-33.45, -70.66]

  return (
    <MapContainer
      center={center}
      zoom={zoom ?? 5}
      scrollWheelZoom={false}
      style={{ height: '100%', width: '100%' }}
      className="z-0"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
      />
      <FitBounds schools={schools} zoom={zoom} />
      {schools.map((s) => (
        <Marker key={s.id} position={[s.lat, s.lng]} icon={makeIcon(s.id === activeId)}>
          <Popup>
            <div style={{ minWidth: 180 }}>
              <strong style={{ fontSize: 14 }}>{s.shortName}</strong>
              <div style={{ fontSize: 12, color: '#666', marginTop: 2 }}>
                {s.comuna}, {s.region}
              </div>
              <Link
                href={`/liceos/${s.id}`}
                style={{
                  display: 'inline-block',
                  marginTop: 8,
                  fontSize: 12,
                  fontWeight: 600,
                  color: 'oklch(0.54 0.21 264)',
                }}
              >
                Ver perfil →
              </Link>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  )
}
