"""
InnoVerse AI 2.0 — Channel-Aware Message Formatter
====================================================
Formats messages appropriately for each communication channel.
Telegram: concise, emoji, action-oriented
Email: formal, detailed HTML, executive summaries
Discord: team-oriented, structured, embeds
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class ChannelFormatter:
    """Formats messages per channel conventions."""

    @staticmethod
    def format_innovation_summary(channel: str, project_data: Dict[str, Any]) -> Dict[str, str]:
        """Format innovation analysis summary for the given channel."""
        score = project_data.get("overall_score", 0)
        title = project_data.get("title", "Innovation Project")
        recommendation = project_data.get("recommendation", "Pending")
        confidence = project_data.get("confidence", 0)

        if channel == "telegram":
            return ChannelFormatter._telegram_summary(title, score, recommendation, confidence, project_data)
        elif channel == "email":
            return ChannelFormatter._email_summary(title, score, recommendation, confidence, project_data)
        elif channel == "discord":
            return ChannelFormatter._discord_summary(title, score, recommendation, confidence, project_data)
        else:
            return {"text": f"Innovation Score: {score}/100 — {recommendation}"}

    @staticmethod
    def _telegram_summary(title: str, score: float, rec: str, confidence: float,
                          data: Dict[str, Any]) -> Dict[str, str]:
        score_emoji = "🟢" if score >= 75 else "🟡" if score >= 50 else "🔴"
        text = (
            f"🧠 *InnoVerse AI Analysis Complete*\n\n"
            f"📋 *{title}*\n"
            f"{score_emoji} Innovation Score: *{score}/100*\n"
            f"🎯 Confidence: {confidence:.0%}\n"
            f"📌 Recommendation: *{rec}*\n\n"
        )

        # Add top risks if available
        risks = data.get("top_risks", [])
        if risks:
            text += "⚠️ *Key Risks:*\n"
            for r in risks[:3]:
                text += f"  • {r}\n"
            text += "\n"

        # Add next steps if available
        tasks = data.get("next_steps", [])
        if tasks:
            text += "📝 *Next Steps:*\n"
            for i, t in enumerate(tasks[:3], 1):
                text += f"  {i}. {t}\n"
            text += "\n"

        text += "💬 Reply with updates or questions."
        return {"text": text}

    @staticmethod
    def _email_summary(title: str, score: float, rec: str, confidence: float,
                       data: Dict[str, Any]) -> Dict[str, str]:
        score_color = "#22c55e" if score >= 75 else "#eab308" if score >= 50 else "#ef4444"

        html = f"""
        <div style="font-family: Inter, Arial, sans-serif; max-width: 640px; margin: 0 auto; color: #1e293b;">
            <div style="background: linear-gradient(135deg, #0f172a, #1e293b); padding: 32px; border-radius: 16px 16px 0 0;">
                <h1 style="color: #f1f5f9; font-size: 24px; margin: 0 0 8px;">🧠 InnoVerse AI — Innovation Report</h1>
                <p style="color: #94a3b8; font-size: 14px; margin: 0;">{title}</p>
            </div>

            <div style="background: #fff; padding: 32px; border: 1px solid #e2e8f0;">
                <div style="display: flex; gap: 24px; margin-bottom: 24px;">
                    <div style="text-align: center; flex: 1; padding: 16px; background: #f8fafc; border-radius: 12px;">
                        <div style="font-size: 36px; font-weight: 900; color: {score_color};">{score}</div>
                        <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Innovation Score</div>
                    </div>
                    <div style="text-align: center; flex: 1; padding: 16px; background: #f8fafc; border-radius: 12px;">
                        <div style="font-size: 36px; font-weight: 900; color: #3b82f6;">{confidence:.0%}</div>
                        <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Confidence</div>
                    </div>
                </div>

                <h2 style="font-size: 18px; color: #0f172a; margin: 24px 0 12px;">Recommendation</h2>
                <p style="font-size: 15px; color: #334155; line-height: 1.6;">{rec}</p>
        """

        # Executive summary
        exec_summary = data.get("executive_summary", "")
        if exec_summary:
            html += f"""
                <h2 style="font-size: 18px; color: #0f172a; margin: 24px 0 12px;">Executive Summary</h2>
                <p style="font-size: 14px; color: #475569; line-height: 1.7;">{exec_summary}</p>
            """

        # Score breakdown
        score_breakdown = data.get("score_breakdown", {})
        if score_breakdown:
            html += '<h2 style="font-size: 18px; color: #0f172a; margin: 24px 0 12px;">Score Breakdown</h2>'
            html += '<table style="width: 100%; border-collapse: collapse; font-size: 13px;">'
            for dim, val in score_breakdown.items():
                bar_width = max(0, min(100, float(val) if isinstance(val, (int, float)) else 0))
                dim_label = dim.replace("_", " ").title()
                html += f"""
                <tr>
                    <td style="padding: 8px 0; color: #64748b; width: 40%;">{dim_label}</td>
                    <td style="padding: 8px 0;">
                        <div style="background: #f1f5f9; border-radius: 4px; height: 8px; width: 100%;">
                            <div style="background: {score_color}; border-radius: 4px; height: 8px; width: {bar_width}%;"></div>
                        </div>
                    </td>
                    <td style="padding: 8px 8px; color: #0f172a; font-weight: 700; width: 40px; text-align: right;">{bar_width:.0f}</td>
                </tr>"""
            html += '</table>'

        # Risks
        risks = data.get("top_risks", [])
        if risks:
            html += '<h2 style="font-size: 18px; color: #0f172a; margin: 24px 0 12px;">⚠️ Key Risks</h2><ul style="font-size: 14px; color: #475569;">'
            for r in risks[:5]:
                html += f'<li style="margin-bottom: 6px;">{r}</li>'
            html += '</ul>'

        # Tasks
        tasks = data.get("next_steps", [])
        if tasks:
            html += '<h2 style="font-size: 18px; color: #0f172a; margin: 24px 0 12px;">📋 Execution Plan</h2><ol style="font-size: 14px; color: #475569;">'
            for t in tasks[:8]:
                html += f'<li style="margin-bottom: 6px;">{t}</li>'
            html += '</ol>'

        html += """
            </div>
            <div style="background: #f8fafc; padding: 16px 32px; border-radius: 0 0 16px 16px; border: 1px solid #e2e8f0; border-top: none;">
                <p style="font-size: 12px; color: #94a3b8; margin: 0; text-align: center;">
                    Powered by InnoVerse AI 2.0 — Autonomous Multi-Agent Innovation Platform
                </p>
            </div>
        </div>
        """

        plain_text = (
            f"InnoVerse AI — Innovation Report\n\n"
            f"Project: {title}\n"
            f"Innovation Score: {score}/100\n"
            f"Confidence: {confidence:.0%}\n"
            f"Recommendation: {rec}\n\n"
            f"{exec_summary}\n"
        )

        return {"text": plain_text, "html": html}

    @staticmethod
    def _discord_summary(title: str, score: float, rec: str, confidence: float,
                         data: Dict[str, Any]) -> Dict[str, str]:
        score_bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
        text = (
            f"## 🧠 InnoVerse AI Analysis Complete\n\n"
            f"**{title}**\n\n"
            f"```\n"
            f"Innovation Score: [{score_bar}] {score}/100\n"
            f"Confidence:       {confidence:.0%}\n"
            f"Recommendation:   {rec}\n"
            f"```\n\n"
        )

        risks = data.get("top_risks", [])
        if risks:
            text += "**⚠️ Key Risks:**\n"
            for r in risks[:3]:
                text += f"- {r}\n"
            text += "\n"

        tasks = data.get("next_steps", [])
        if tasks:
            text += "**📋 Next Steps:**\n"
            for i, t in enumerate(tasks[:5], 1):
                text += f"{i}. {t}\n"

        text += "\n*Reply with task updates to track progress.*"
        return {"text": text}

    @staticmethod
    def format_task_reminder(channel: str, task_title: str,
                             progress: int, total: int,
                             project_title: str = "") -> Dict[str, str]:
        """Format a task follow-up reminder."""
        if channel == "telegram":
            return {"text": (
                f"📌 *Task Reminder*\n\n"
                f"📋 {task_title}\n"
                f"📊 Progress: {progress}/{total}\n"
                f"{'🔹 ' + project_title if project_title else ''}\n\n"
                f"Reply with your update or type DONE when complete."
            )}
        elif channel == "email":
            return {
                "text": f"Task Reminder: {task_title} — Progress: {progress}/{total}",
                "html": f"""
                <div style="font-family: Inter, Arial, sans-serif; max-width: 480px; margin: 0 auto;">
                    <h2 style="color: #0f172a;">📌 Task Reminder</h2>
                    <p><strong>{task_title}</strong></p>
                    <p>Progress: <strong>{progress}/{total}</strong></p>
                    <p style="color: #64748b; font-size: 13px;">Reply to this email with your update.</p>
                </div>
                """
            }
        else:
            return {"text": f"📌 **Task Reminder:** {task_title} — Progress: {progress}/{total}"}

    @staticmethod
    def format_approval_request(channel: str, action: str,
                                project_title: str = "") -> Dict[str, str]:
        """Format an approval request."""
        if channel == "telegram":
            return {"text": (
                f"🔐 *Approval Required*\n\n"
                f"📋 {project_title}\n"
                f"📝 Action: {action}\n\n"
                f"Reply *APPROVE* to proceed or *REJECT* to cancel."
            )}
        elif channel == "email":
            return {
                "text": f"Approval Required: {action}",
                "html": f"""
                <div style="font-family: Inter, Arial, sans-serif; max-width: 480px; margin: 0 auto;">
                    <h2 style="color: #0f172a;">🔐 Approval Required</h2>
                    <p><strong>Project:</strong> {project_title}</p>
                    <p><strong>Action:</strong> {action}</p>
                    <p style="margin-top: 24px;">Reply with <strong>APPROVE</strong> or <strong>REJECT</strong>.</p>
                </div>
                """
            }
        else:
            return {"text": f"🔐 **Approval Required:** {action}\nReply `APPROVE` or `REJECT`."}

    @staticmethod
    def format_score_change(channel: str, old_score: float, new_score: float,
                            reason: str, project_title: str = "") -> Dict[str, str]:
        """Format a score change notification."""
        direction = "📈" if new_score > old_score else "📉"
        change = new_score - old_score

        if channel == "telegram":
            return {"text": (
                f"{direction} *Innovation Score Updated*\n\n"
                f"📋 {project_title}\n"
                f"Score: {old_score} → *{new_score}* ({'+' if change > 0 else ''}{change:.1f})\n\n"
                f"📝 Reason: {reason}"
            )}
        elif channel == "email":
            return {
                "text": f"Score Update: {old_score} → {new_score} for {project_title}",
                "html": f"""
                <div style="font-family: Inter, Arial, sans-serif; max-width: 480px; margin: 0 auto;">
                    <h2 style="color: #0f172a;">{direction} Innovation Score Updated</h2>
                    <p><strong>{project_title}</strong></p>
                    <p style="font-size: 24px; font-weight: 900;">{old_score} → {new_score}</p>
                    <p style="color: #64748b;">{reason}</p>
                </div>
                """
            }
        else:
            return {"text": f"{direction} **Score Update:** {old_score} → {new_score} — {reason}"}


channel_formatter = ChannelFormatter()
