
"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { QRCodeSVG } from "qrcode.react";
import { api } from "@/lib/api";

type Payment = {
  id: string;
  amount: string;
  currency: string;
  network: string;
  status: string;
  payment_url: string;
};

const TEST_PAYMENT_ID = "e31559eb-8d2b-4be3-ac2d-73f1d6c168e5";

export default function Home() {
  const [showPayment, setShowPayment] = useState(false);

  const {
    data: payment,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["payment", TEST_PAYMENT_ID],
    queryFn: () =>
      api<Payment>(`/api/public/v1/payments/${TEST_PAYMENT_ID}`),
    enabled: showPayment,
    refetchInterval: (query) =>
      query.state.data?.status === "paid" ? false : 5000,
  });

  const checkoutUrl =
    payment && typeof window !== "undefined"
      ? `${window.location.origin}/pay/${payment.id}`
      : "";

  return (
    <main className="flex min-h-screen items-center justify-center bg-zinc-50 p-6 font-sans dark:bg-black">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 text-center shadow-lg">
        <h1 className="mb-2 text-2xl font-semibold text-zinc-900">
          Crypto Payment
        </h1>

        {!showPayment ? (
          <button
            onClick={() => setShowPayment(true)}
            className="mt-6 rounded-xl bg-black px-6 py-3 text-white"
          >
            Show Payment
          </button>
        ) : isLoading ? (
          <p className="mt-6 text-zinc-500">
            Loading payment...
          </p>
        ) : isError || !payment ? (
          <p className="mt-6 text-red-600">
            Payment not found.
          </p>
        ) : (
          <div className="mt-6 flex flex-col items-center gap-5">
            <div>
              <p className="text-3xl font-bold text-zinc-900">
                {payment.amount} {payment.currency}
              </p>
              <p className="mt-1 text-sm text-zinc-500">
                Solana Devnet
              </p>
            </div>

            <div className="rounded-xl border border-zinc-200 bg-white p-5">
              <QRCodeSVG
                value={checkoutUrl}
                size={240}
                level="M"
              />
            </div>

            <p className="text-sm text-zinc-500">
              Scan to open the payment page
            </p>

            <span className="rounded-full bg-amber-100 px-4 py-2 text-sm font-medium text-amber-800">
              {payment.status}
            </span>

            <button
              onClick={() =>
                navigator.clipboard.writeText(checkoutUrl)
              }
              className="text-sm font-medium text-blue-600 hover:underline"
            >
              Copy payment link
            </button>
          </div>
        )}
      </div>
    </main>
  );
}
