"use client";

import {
  useEffect,
  useState,
} from "react";

import {
  CustomerSession,
  securityService,
} from "@/services/security";

import DataTable from "@/components/admin/DataTable";


export default function CustomerSessionTab() {

  const [
    sessions,
    setSessions,
  ] = useState<CustomerSession[]>([]);

  const [
    loading,
    setLoading,
  ] = useState(true);


  const fetchData = async () => {

    setLoading(true);

    try {

      const data =
        await securityService.getCustomerSessions({
          limit: 100,
        });

      setSessions(data.items);

    } catch (error) {

      console.error(
        "Failed to load customer sessions:",
        error
      );

    } finally {

      setLoading(false);

    }

  };


  useEffect(() => {

    fetchData();

  }, []);


  const getStatus = (
    session: CustomerSession
  ) => {

    if (session.revoked_at) {
      return "Revoked";
    }

    if (
      new Date(session.expires_at).getTime()
      <= Date.now()
    ) {
      return "Expired";
    }

    return "Active";

  };


  const getDevice = (
    session: CustomerSession
  ) => {

    const values = [
      session.device_name,
      session.browser,
      session.operating_system,
    ].filter(Boolean);

    if (values.length === 0) {
      return "Unknown";
    }

    return values.join(" / ");

  };


  const getLocation = (
    session: CustomerSession
  ) => {

    const values = [
      session.city,
      session.country,
    ].filter(Boolean);

    if (values.length === 0) {
      return "Unknown";
    }

    return values.join(", ");

  };


  const handleRevoke = async (
    publicId: string
  ) => {

    if (
      !confirm(
        "Revoke this customer session?"
      )
    ) {
      return;
    }

    try {

      await securityService.revokeCustomerSession(
        publicId
      );

      await fetchData();

    } catch (error) {

      console.error(
        "Failed to revoke session:",
        error
      );

    }

  };


  const tableData = sessions.map(
    (session) => ({

      ...session,

      session_id:
        session.public_id.length > 12
          ? `${session.public_id.slice(0, 12)}...`
          : session.public_id,

      device:
        getDevice(session),

      location:
        getLocation(session),

      status:
        getStatus(session),

    })
  );


  return (

    <div>

      <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4 mb-4">

        <button
          onClick={fetchData}
          className="w-full sm:w-auto bg-black text-white px-4 py-2 rounded"
        >
          Refresh
        </button>

      </div>


      {loading ? (

        <div>
          Loading...
        </div>

      ) : (

        <DataTable

          columns={[

            {
              key: "session_id",
              label: "Session",
            },

            {
              key: "customer_id",
              label: "Customer",
            },

            {
              key: "ip_address",
              label: "IP",
            },

            {
              key: "device",
              label: "Device",
            },

            {
              key: "location",
              label: "Location",
            },

            {
              key: "login_at",
              label: "Login Time",

              render: (value) =>
                typeof value === "string"
                  ? new Date(
                      value
                    ).toLocaleString()
                  : "",
            },

            {
              key: "last_activity",
              label: "Last Activity",

              render: (value) =>
                typeof value === "string"
                  ? new Date(
                      value
                    ).toLocaleString()
                  : "",
            },

            {
              key: "status",
              label: "Status",
            },

          ]}

          data={tableData}

          onDelete={(row) =>
            row.status === "Active"
              ? handleRevoke(row.public_id)
              : undefined
          }

          deleteLabel="Revoke"

        />

      )}

    </div>

  );

}