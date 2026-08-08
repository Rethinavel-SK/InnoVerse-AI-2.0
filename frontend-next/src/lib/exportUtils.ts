import { InnovationReport } from "./types";

export function exportToMarkdown(report: InnovationReport, title: string = "Innovation Report"): string {
  const score = report.overall_innovation_score ?? report.feasibility_score ?? 85;
  const confidence = report.confidence ? `${Math.round(report.confidence * 100)}%` : "90%";
  const rec = typeof report.final_recommendation === "object"
    ? report.final_recommendation?.build_recommendation ?? report.recommendation ?? "GO"
    : report.recommendation ?? "GO";

  let md = `# ${title}\n\n`;
  md += `**Overall Innovation Score:** ${score}/100\n`;
  md += `**Confidence Score:** ${confidence}\n`;
  md += `**Build Recommendation:** ${rec}\n\n`;
  md += `---\n\n`;

  md += `## Executive Summary\n${report.executive_summary}\n\n`;
  md += `## Problem Understanding\n${report.problem_understanding}\n\n`;

  if (report.technical_summary) {
    md += `## Technical Architecture\n`;
    if (report.technical_summary.architecture) {
      md += `**Architecture Style:** ${report.technical_summary.architecture.type}\n`;
      if (report.technical_summary.architecture.rationale) {
        md += `*Rationale:* ${report.technical_summary.architecture.rationale}\n`;
      }
    }
    if (report.technical_summary.estimated_complexity) {
      md += `**Estimated Complexity:** ${report.technical_summary.estimated_complexity}\n`;
    }
    if (report.technical_summary.prototype_cost) {
      md += `**Prototype Cost:** ${report.technical_summary.prototype_cost}\n`;
    }
    md += `\n`;
  }

  if (report.business_summary) {
    md += `## Business Strategy\n`;
    if (report.business_summary.business_model) md += `**Business Model:** ${report.business_summary.business_model}\n`;
    if (report.business_summary.value_proposition) md += `**Value Proposition:** ${report.business_summary.value_proposition}\n`;
    if (report.business_summary.pricing_model) md += `**Pricing Model:** ${report.business_summary.pricing_model}\n`;
    md += `\n`;
  }

  if (report.risk_summary) {
    md += `## Risk Assessment\n`;
    if (report.risk_summary.overall_risk_score !== undefined) md += `**Risk Score:** ${report.risk_summary.overall_risk_score}/100 (${report.risk_summary.risk_level ?? "Medium"} Risk)\n`;
    if (report.risk_summary.summary) md += `${report.risk_summary.summary}\n`;
    md += `\n`;
  }

  if (report.roadmap_summary) {
    md += `## MVP & Roadmap\n`;
    if (report.roadmap_summary.timeline) md += `**Timeline:** ${report.roadmap_summary.timeline}\n`;
    if (report.roadmap_summary.estimated_budget) md += `**Estimated Budget:** ${report.roadmap_summary.estimated_budget}\n`;
    if (report.roadmap_summary.team_size) md += `**Team Size:** ${report.roadmap_summary.team_size}\n`;
    md += `\n`;
  }

  return md;
}

export function downloadFile(content: string, filename: string, type: string) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export function downloadMarkdownReport(report: InnovationReport, id: string) {
  const md = exportToMarkdown(report, `Innovation Report - ${id}`);
  downloadFile(md, `innovation_report_${id}.md`, "text/markdown;charset=utf-8;");
}

export function downloadDOCXReport(report: InnovationReport, id: string) {
  const md = exportToMarkdown(report, `Innovation Report - ${id}`);
  downloadFile(md, `innovation_report_${id}.docx`, "application/vnd.openxmlformats-officedocument.wordprocessingml.document;charset=utf-8;");
}

export function downloadJSONReport(report: InnovationReport, id: string) {
  downloadFile(JSON.stringify(report, null, 2), `innovation_report_${id}.json`, "application/json;charset=utf-8;");
}
