"use client"

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

interface Transaction {
  id: string;
  date: string;
  description: string;
  transaction_type: string;
  amount: number;
  balance: number;
  currency: string;
}

interface TransactionsTableProps {
  transactions: Transaction[];
}

export function TransactionsTable({ transactions }: TransactionsTableProps) { // Receive transactions as a prop
  return (
    <Table>
      <TableHeader>
        <TableRow className="border-gray-200">
          <TableHead className="text-gray-900 sticky top-0">Date</TableHead>
          <TableHead className="text-gray-900 sticky top-0">Description</TableHead>
          <TableHead className="text-gray-900 sticky top-0">Type</TableHead>
          <TableHead className="text-gray-900 text-right sticky top-0">Amount</TableHead>
          <TableHead className="text-gray-900 text-right sticky top-0">Balance</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {transactions.map((transaction) => (
          <TableRow key={transaction.id} className="border-gray-200 transition-colors hover:bg-gray-100">
            <TableCell className="font-medium text-gray-900">
              {new Date(transaction.date).toLocaleDateString()}
            </TableCell>
            <TableCell className="text-gray-700">{transaction.description}</TableCell>
            <TableCell className="text-gray-700 capitalize">{transaction.transaction_type}</TableCell>
            <TableCell
              className={`text-right ${transaction.transaction_type === "debit" ? "text-red-600" : "text-green-600"}`}
            >
              {transaction.transaction_type === "debit" ? "-" : "+"}
              {transaction.currency} {transaction.amount.toFixed(2)}
            </TableCell>
            <TableCell className="text-right text-gray-900">{transaction.currency} {transaction.balance.toFixed(2)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}