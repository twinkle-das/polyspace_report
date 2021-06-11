<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:template match="root">
        <html>
            <head>
                <meta charset="UTF-8"></meta>
                <style type="text/css">
					table.report_main {
						border-collapse: collapse;
						width: 100%;
					}
					table.report_main tr th {
						font-weight: bold;
						background:#5082ba;
						color:#ffffff;
						font-size:14px;
						border: 1px solid;
					}
					 table.report_main tr td {
						color:#000000;
						border: 0.5px solid black;
						font-size:12px;
						border-collapse:collapse;
						word-wrap:break-word;
					}
                    h4 {
                        margin: 15px 0;
                    }
					th,td {
						text-align: left;
						padding: 8px;
					}
                    tr:nth-child(odd) {
                        background: #e9ebf2;
                    }
                    tr:nth-child(even) {
                        background: #d1d7e6;
                    } input[name="collapse"] {
                        display: none;
                    }
						
                </style>
            </head>
            <body style="font-family:Arial">
                <h4>
                    <b>Summary: </b>
                </h4>
                <table class="report_main" style="table-layout:fixed">
						<tr>
							<th width="25%">Property</th>
							<th width="35%">Value</th>
							<th width="40%">Reference Links</th>
						</tr>
						<tr>
							<td>Build ID</td>
							<td>
								<xsl:value-of select="Build_ID"/> - <xsl:value-of select="Build_Type"/>
							</td>
							<td></td>
						</tr>
						<tr>
							<td>Job Name</td>
							<td>
								<xsl:value-of select="Job_Name"/>
							</td>
							<td></td>
						</tr>
                        <tr>
							<td>Job Status</td>
							<td>
                                <xsl:if test="not(Job_Status)">
									<b style='color: red;'>Aborted</b>
								</xsl:if>
								<xsl:if test="Job_Status='Successful'">
									<b>Successful</b>
								</xsl:if>
								<xsl:if test="Job_Status='Failure'">
									<b style='color: red;'>Failure</b>
								</xsl:if>
							</td>
							<td></td>
						</tr>
						<tr>
							<td>Job URL</td>
							<td>
								<a href="{Job_URL}"><xsl:value-of select="Job_URL"/></a>
							</td>
							<td></td>
						</tr>
						<tr>
							<td>Build Trigger Time</td>
							<td>
								<xsl:value-of select="Build_Trigger_Time"/>
							</td>
							<td></td>
						</tr>
                        <tr>
                            <td>Quality Analysis</td>
                            <td>
								<xsl:if test="not(Quality_Analysis)">
									<b style='color: red;'>Aborted</b>
								</xsl:if>
                                <xsl:if test="Quality_Analysis='Failure'">
                                    <xsl:value-of select="Total_Violation"/><b style='color: red;'> [Failure]</b>
                                </xsl:if>
                                <xsl:if test="Quality_Analysis='Successful'">
                                    <xsl:value-of select="Total_Violation"/><b> [Successful]</b>
                                </xsl:if>
                            </td>
                            <td><a href="{Polyspace_report_url}"><xsl:value-of select="Polyspace_report_url"/></a></td>
                        </tr>
					</table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>