import axios from 'axios';

export const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL || '' });

export type RiskLevel = 'low' | 'medium' | 'high';
export const riskLabel: Record<string, string> = { low: '低风险', medium: '中风险', high: '高风险' };
export const riskColor: Record<string, string> = { low: 'green', medium: 'orange', high: 'red' };
export const statusLabel: Record<string, string> = { pending: '待随访', completed: '已完成', overdue: '已逾期' };

export interface RiskAssessment {
  id: number;
  model_version: string;
  probability: number;
  risk_level: RiskLevel;
  explanation: string;
  disclaimer: string;
  created_at: string;
}

export interface FollowupPlan {
  id: number;
  patient_id: number;
  demo_code?: string;
  title: string;
  scheduled_date: string;
  status: string;
  checklist: string;
}

export interface Patient {
  id: number;
  demo_code: string;
  sex: string;
  age: number;
  surgery_date: string;
  asthma: boolean;
  allergic_rhinitis: boolean;
  prior_surgery_count: number;
  eosinophil_percent: number;
  tissue_eosinophil_level: number;
  snot22_score: number;
  polyp_score: number;
  adherence_score: number;
  treatment_plan: string;
  risk_assessments: RiskAssessment[];
  followup_plans: FollowupPlan[];
}
