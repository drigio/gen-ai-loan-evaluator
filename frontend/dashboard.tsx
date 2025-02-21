// Filename: app/dashboard.tsx
"use client"

import { useState, useEffect } from "react"
import { ArrowUpRight, Download, FileText, MoreHorizontal, Upload } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"

import { TransactionsTable } from "./transactions-table"
import { ScoreGauge } from "./score-gauge"
import { FinancialMetric } from "./financial-metric"
import { MonthlyChart } from "./monthly-chart"
import { ExpensePieChart } from "./expense-pie-chart"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "./components/ui/tooltip"

import { fetchApplicantData } from "./lib/api"
import { LoadingOverlay } from "./components/ui/loading-overlay"

// Define interfaces for the data structures
interface Transaction {
  id: string;
  date: string;
  description: string;
  transaction_type: string;
  amount: number;
  balance: number;
  currency: string;
}

interface KeyFinancialIndicators {
  monthly_income: number;
  monthly_expenses: number;
  net_monthly_income: number;
  income_coefficient_of_variation: number;
  expense_coefficient_of_variation: number;
  savings_rate: number;
  average_account_balance: number;
  liquidity_ratio: number;
  number_of_overdrafts: number;
  income_stability_score: number;
  expense_stability_score: number;
  savings_rate_score: number;
  liquidity_ratio_score: number;
  overdraft_penalty_score: number;
  id?: string; // Add id, as it might be present in the actual response
}
interface ApplicantData {
  id: string;
  name: string;
  bank_statement_pdf_path: string | null;
  raw_bank_statement_txt: string | null;
  transactions: Transaction[] | null;
  key_financial_indicators: KeyFinancialIndicators | null;
}

interface DashboardProps {
  applicantId: string;
  onReset: () => void;
}

export default function Dashboard({ applicantId, onReset }: DashboardProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [applicantData, setApplicantData] = useState<ApplicantData | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);

  // Hardcoded applicant ID for now
  // const applicantId = "67a3ddf0b6ea8f6228532a61";

  useEffect(() => {

    async function fetchData() {
      try {
        const data: ApplicantData | null = await fetchApplicantData(applicantId);
        if (data) {
          setApplicantData(data);
          const timer = setTimeout(() => {
            setIsLoaded(true);
          }, 300); // Short delay for smoother animation
          return () => clearTimeout(timer)
        } else {
          console.log("No applicant data found for applicant.");
          setApplicantData(null); // Set to null for no data
        }
      } catch (error) {
        console.error("Error fetching applicant data:", error);
        setApplicantData(null); // Set to null on error
      }
    }

    fetchData();
  }, [applicantId]);


  if (!applicantData) {
    return <LoadingOverlay />
    // return <div>Loading...</div>; // Or a more sophisticated loading indicator
  }

  // Get the currency from the first transaction, or default to USD
  const currency = applicantData.transactions && applicantData.transactions.length > 0
    ? applicantData.transactions[0].currency
    : "USD";

  // const overallScore = applicantData?.key_financial_indicators ? Math.round(
  //   (applicantData.key_financial_indicators.income_stability_score +
  //     applicantData.key_financial_indicators.expense_stability_score +
  //     applicantData.key_financial_indicators.savings_rate_score +
  //     applicantData.key_financial_indicators.liquidity_ratio_score +
  //     applicantData.key_financial_indicators.overdraft_penalty_score) *
  //   20,
  // ) : 0;

  const calculateOverallScore = () => { // Define as a separate function
    if (applicantData?.key_financial_indicators) {
      const kfi = applicantData.key_financial_indicators;
      const weights = {
        incomeStability: 0.20,
        expenseStability: 0.05,
        savingsRate: 0.35,
        liquidityRatio: 0.40,
        // overdraftPenalty: 0.20,
      };

      const weightedScore = (
        kfi.income_stability_score * weights.incomeStability +
        kfi.expense_stability_score * weights.expenseStability +
        kfi.savings_rate_score * weights.savingsRate +
        kfi.liquidity_ratio_score * weights.liquidityRatio
        // +
        // kfi.overdraft_penalty_score * weights.overdraftPenalty
      );

      const normalizedScore = Math.round(weightedScore * 100);
      return Math.max(0, Math.min(100, normalizedScore));
    }
    return 0; // Default return outside the if
  };

  // Aggregate transactions by month
  const monthlyData: { [key: string]: { credit: number; debit: number } } = {};

  if (applicantData?.transactions) {
    for (const transaction of applicantData.transactions) {
      const date = new Date(transaction.date);
      const monthYear = `${date.toLocaleString('default', { month: 'short' })}-${date.getFullYear()}`; // e.g., "Jan-2023"

      if (!monthlyData[monthYear]) {
        monthlyData[monthYear] = { credit: 0, debit: 0 };
      }

      if (transaction.transaction_type === 'credit') {
        monthlyData[monthYear].credit += transaction.amount;
      } else if (transaction.transaction_type === 'debit') {
        monthlyData[monthYear].debit += transaction.amount;
      }
    }
  }

  // Convert the aggregated data to the format required by the chart
  const chartData = Object.entries(monthlyData).map(([monthYear, data]) => ({
    month: monthYear,
    credit: data.credit,
    debit: data.debit,
    currency: currency
  }));

  chartData.sort((a, b) => {
    const [aMonth, aYear] = a.month.split('-');
    const [bMonth, bYear] = b.month.split('-');
    const dateA = new Date(`${aMonth} 01 ${aYear}`);
    const dateB = new Date(`${bMonth} 01 ${bYear}`);
    return dateA.getTime() - dateB.getTime();
  });

  return (
    <div className="flex min-h-screen flex-col bg-[url('/bg.png')] bg-repeat">
      <div
        className={`transition-all duration-500 ease-in-out ${
          isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
        }`}
      >
        <header className="top-0 z-0 w-full border-b border-border/40 bg-header-dark text-white">
          <div className="px-24 h-16 flex max-w-screen items-center">
            <div className="hidden md:flex">
              <a className="flex items-center" href="/">
                <span className="font-sans hidden font-bold sm:inline-block text-xl subpixel-antialiased ">SaraFi</span>
              </a>
            </div>
            <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
              <Avatar className=" h-6 w-6" onClick={onReset} style={{ cursor: 'pointer' }}>
                <AvatarImage src="https://avatar.iran.liara.run/public/30" alt="User Avatar" />
                <AvatarFallback>U</AvatarFallback>
              </Avatar>
            </div>
          </div>
          <div className="mx-24 pb-4">
            <Separator className="mb-6 bg-gray-700 " />
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-2xl font-bold tracking-tight">{applicantData?.name}</h2>
              <div className="flex items-center space-x-2">
                <Button variant="outline" className="bg-gray-700 border-0 rounded-none mr-2">
                  <Download className="mr-2 h-4 w-4" />
                  Download Report
                </Button>
              </div>
            </div>
          </div>
        </header>

        <div className="-mt-6 mb-12 flex-1 z-50 space-y-4 px-24 text-gray-900">
          <div className="grid grid-cols-8 gap-4">
            <div className="col-span-5 grid gap-4 md:grid-cols-2 lg:grid-cols-4 p-6 rounded-md bg-main-light shadow-sm border-[1px]">
              <div className="col-span-8 -mt-2">
                <span className="text-xl font-bold text-gray-700 ml-2">Applicant Information</span>
              </div>
              <Card className="bg-main-dark border-gray-200 shadow-sm">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium text-gray-300">Income Stability Score</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xl font-bold text-gray-100">{applicantData.key_financial_indicators?.income_stability_score.toFixed(2)}</div>
                  <p className="text-xs text-gray-500">Based on income data</p>
                </CardContent>
              </Card>
              <Card className="bg-main-dark border-gray-200 shadow-sm">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium text-gray-300">Expense Stability Score</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xl font-bold text-gray-100">{applicantData.key_financial_indicators?.expense_stability_score.toFixed(2)}</div>
                  <p className="text-xs text-gray-500">Based on expense data</p>
                </CardContent>
              </Card>
              <Card className="bg-main-dark border-gray-200 shadow-sm">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium text-gray-300">Liquidity Ratio Score</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xl font-bold text-gray-100">{applicantData.key_financial_indicators?.liquidity_ratio_score.toFixed(2)}</div>
                  <p className="text-xs text-gray-500">Based on liquidity data</p>
                </CardContent>
              </Card>
              <Card className="bg-main-dark border-gray-200 shadow-sm">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium text-gray-300">Savings Rate Score</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xl font-bold text-gray-100">{applicantData.key_financial_indicators?.savings_rate_score.toFixed(2)}</div>
                  <p className="text-xs text-gray-500">Based on savings data</p>
                </CardContent>
              </Card>


              <div className="col-span-full flex flex-wrap gap-x-4 gap-y-2 justify-center bg-main-light pt-2 ">
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Card className="bg-main-light border-gray-400 shadow-sm rounded-sm mb-2 border-[1px]">
                        <CardHeader className="flex flex-row items-center justify-evenly space-y-0 p-4 ">
                          <CardTitle className="text-sm font-bold text-gray-800">AMI</CardTitle>
                          <div className="text-sm px-2 font-medium text-gray-500"> | {currency} {applicantData.key_financial_indicators?.monthly_income.toFixed(2)}</div>
                        </CardHeader>
                      </Card>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Average Monthly Income</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Card className="bg-main-light border-gray-400 shadow-sm rounded-sm mb-2 border-[1px]">
                        <CardHeader className="flex flex-row items-center justify-evenly space-y-0 p-4 ">
                          <CardTitle className="text-sm font-bold text-gray-800">AME</CardTitle>
                          <div className="text-sm px-2 font-medium text-gray-500"> | {currency} {applicantData.key_financial_indicators?.monthly_expenses.toFixed(2)}</div>
                        </CardHeader>
                      </Card>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Average Monthly Expense</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Card className="bg-main-light border-gray-400 shadow-sm rounded-sm mb-2 border-[1px]">
                        <CardHeader className="flex flex-row items-center justify-evenly space-y-0 p-4 ">
                          <CardTitle className="text-sm font-bold text-gray-800">NMI</CardTitle>
                          <div className="text-sm px-2 font-medium text-gray-500"> | {currency} {applicantData.key_financial_indicators?.net_monthly_income.toFixed(2)}</div>
                        </CardHeader>
                      </Card>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Net Monthly Income</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Card className="bg-main-light border-gray-400 shadow-sm rounded-sm mb-2 border-[1px]">
                        <CardHeader className="flex flex-row items-center justify-evenly space-y-0 p-4 ">
                          <CardTitle className="text-sm font-bold text-gray-800">ICoV</CardTitle>
                          <div className="text-sm px-2 font-medium text-gray-500"> | {applicantData.key_financial_indicators?.income_coefficient_of_variation.toFixed(2)}</div>
                        </CardHeader>
                      </Card>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Income Coefficient of Variation</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Card className="bg-main-light border-gray-400 shadow-sm rounded-sm mb-2 border-[1px]">
                        <CardHeader className="flex flex-row items-center justify-evenly space-y-0 p-4 ">
                          <CardTitle className="text-sm font-bold text-gray-800">ECoV</CardTitle>
                          <div className="text-sm px-2 font-medium text-gray-500"> | {applicantData.key_financial_indicators?.expense_coefficient_of_variation.toFixed(2)}</div>
                        </CardHeader>
                      </Card>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Expense Coefficient of Variation</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Card className="bg-main-light border-gray-400 shadow-sm rounded-sm mb-2 border-[1px]">
                        <CardHeader className="flex flex-row items-center justify-evenly space-y-0 p-4 ">
                          <CardTitle className="text-sm font-bold text-gray-800">SR</CardTitle>
                          <div className="text-sm px-2 font-medium text-gray-500"> | {applicantData.key_financial_indicators?.savings_rate.toFixed(2)}</div>
                        </CardHeader>
                      </Card>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Savings Rate</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Card className="bg-main-light border-gray-400 shadow-sm rounded-sm mb-2 border-[1px]">
                        <CardHeader className="flex flex-row items-center justify-evenly space-y-0 p-4 ">
                          <CardTitle className="text-sm font-bold text-gray-800">AMB</CardTitle>
                          <div className="text-sm px-2 font-medium text-gray-500"> | {currency} {applicantData.key_financial_indicators?.average_account_balance.toFixed(2)}</div>
                        </CardHeader>
                      </Card>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Average Monthly Balance</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Card className="bg-main-light border-gray-400 shadow-sm rounded-sm mb-2 border-[1px]">
                        <CardHeader className="flex flex-row items-center justify-evenly space-y-0 p-4 ">
                          <CardTitle className="text-sm font-bold text-gray-800">LR</CardTitle>
                          <div className="text-sm px-2 font-medium text-gray-500"> | {applicantData.key_financial_indicators?.liquidity_ratio.toFixed(2)}</div>
                        </CardHeader>
                      </Card>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Liquidity Ratio</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>

              </div>

            </div>
            <Card className="col-span-3 bg-white border-gray-200 shadow-sm bg-main-light border-[1px]">
              <CardHeader>
                <CardTitle className="text-gray-900">Lending Score Analysis</CardTitle>
                <CardDescription>Overall financial health score based on transactions</CardDescription>
              </CardHeader>
              <CardContent>
                <ScoreGauge score={calculateOverallScore()} />
                <div className="mt-4 grid gap-2">
                  <FinancialMetric label="Income Stability" score={applicantData.key_financial_indicators?.income_stability_score} />
                  <FinancialMetric label="Expense Stability" score={applicantData.key_financial_indicators?.expense_stability_score} />
                  <FinancialMetric label="Savings Rate" score={applicantData.key_financial_indicators?.savings_rate_score} />
                  <FinancialMetric label="Liquidity Ratio" score={applicantData.key_financial_indicators?.liquidity_ratio_score} />
                  {/* <FinancialMetric label="Overdraft Score" score={applicantData.key_financial_indicators?.overdraft_penalty_score} /> */}
                </div>
              </CardContent>
            </Card>
            {/* <div className="col-span-3 rounded-md bg-main-light shadow-sm border-[1px]">

            </div> */}
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-8">
            <Card className="col-span-5 bg-white border-gray-200 shadow-sm bg-main-light border-[1px]">
              <CardHeader>
                <CardTitle className="text-gray-900">Financial Overview</CardTitle>
              </CardHeader>
              <CardContent className="p-8">
                <MonthlyChart chartData={chartData} />
              </CardContent>
            </Card>
            {/* <Card className="col-span-3 bg-white border-gray-200 shadow-sm bg-main-light border-[1px]">
              <CardHeader>
                <CardTitle className="text-gray-900">Expense Categories</CardTitle>
              </CardHeader>
              <CardContent>
                <ExpensePieChart />
              </CardContent>
            </Card> */}
            <Dialog>
              <DialogTrigger asChild>
                <Card className="col-span-3 cursor-pointer bg-white border-gray-200 shadow-sm hover:bg-gray-50 transition-colors bg-main-light border-[1px]">
                  <CardHeader>
                    <CardTitle className="text-gray-900">Show Transactions</CardTitle>
                    <CardDescription>Click to view detailed transaction history</CardDescription>
                  </CardHeader>

                </Card>
              </DialogTrigger>
              <DialogContent className="max-w-4xl bg-white bg-main-light border-[1px]">
                <DialogHeader>
                  <DialogTitle className="text-gray-900">Transaction History</DialogTitle>
                </DialogHeader>
                <ScrollArea className="h-[600px] rounded-md border p-4">
                  <TransactionsTable transactions={applicantData.transactions || []} />
                </ScrollArea>
              </DialogContent>
            </Dialog>
          </div>
          {/* <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
            
            
          </div> */}
        </div>
      </div>
    </div>
  )
}