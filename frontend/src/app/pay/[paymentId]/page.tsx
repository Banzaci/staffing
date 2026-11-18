
"use client";

import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

type Payment = {
  id: string;
  amount: string;
  currency: string;
  network: string;
  status: string;
  payment_url: string;
  enabled_payment_methods: string[];
};

export default function PaymentPage() {
  const { paymentId } = useParams<{ paymentId: string }>();

  const { data, isLoading, isError } = useQuery({
    queryKey: ["payment", paymentId],
    queryFn: () =>
      api<Payment>(`/api/public/v1/payments/${paymentId}`),
    enabled: Boolean(paymentId),
    refetchInterval: (query) =>
      query.state.data?.status === "paid" ? false : 5000,
  });

  if (isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        Loading payment...
      </main>
    );
  }

  if (isError || !data) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        Payment not found.
      </main>
    );
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-sm">
        <h1 className="text-center text-2xl font-semibold text-gray-900">
          Payment
        </h1>

        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500">Amount to pay</p>
          <p className="mt-2 text-4xl font-bold text-gray-900">
            {data.amount} {data.currency}
          </p>
        </div>

        <div className="mt-6 text-center">
          <span className="rounded-full bg-gray-100 px-4 py-2 text-sm text-gray-700">
            {data.status}
          </span>
        </div>

        {data.status === "pending" && (
          <div className="mt-10 space-y-3">
            {data.enabled_payment_methods.includes("usdc") && (
              <a
                href={data.payment_url}
                className="block rounded-xl bg-black px-6 py-4 text-center font-medium text-white hover:bg-gray-800"
              >
                Pay with USDC (Solana)
              </a>
            )}

            {data.enabled_payment_methods.length === 0 && (
              <p className="text-center text-sm text-gray-500">
                No payment methods available.
              </p>
            )}
          </div>
        )}

        {data.status === "paid" && (
          <p className="mt-10 text-center font-medium text-green-600">
            Payment completed
          </p>
        )}

        <p className="mt-8 text-center text-xs text-gray-400">
          Powered by Payment
        </p>
      </div>
    </main>
  );
}
