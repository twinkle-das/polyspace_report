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
					.content{
						display: none;
					}
					.details-btn{
						cursor: pointer;
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
								<xsl:if test="not(Build_ID)">
									<b style='color: red;'>Aborted</b>
								</xsl:if>
								<xsl:choose>
									<xsl:when test="not(Build_Type)">
										<xsl:value-of select="Build_ID"/>
									</xsl:when>
									<xsl:otherwise>
										<xsl:value-of select="Build_ID"/> - <xsl:value-of select="Build_Type"/>
									</xsl:otherwise>
								</xsl:choose>
							</td>
							<td></td>
						</tr>
						<tr>
							<td>Job Name</td>
							<td>
							<xsl:choose>
								<xsl:when test="not(Job_Name)">
									<b style='color: red;'>Aborted</b>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="Job_Name"/>
								</xsl:otherwise>
							</xsl:choose>
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
							<xsl:choose>
								<xsl:when test="not(Job_URL)">
									<b style='color: red;'>Aborted</b>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="Job_URL"/>
								</xsl:otherwise>
							</xsl:choose>
							</td>
							<td></td>
						</tr>
						<tr>
							<td>Build Trigger Time</td>
							<td>
							<xsl:choose>
								<xsl:when test="not(Build_Trigger_Time)">
									<b style='color: red;'>Aborted</b>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="Build_Trigger_Time"/>
								</xsl:otherwise>
							</xsl:choose>
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
						<tr>
							<td>Cyclomatic Complexity</td>
							<td>
								<xsl:value-of select="Cyclomatic_Complexity/max_value"/> [<xsl:value-of select="Cyclomatic_Complexity/file_name/func_name"/>]
							</td>
							<td><xsl:value-of select="Cyclomatic_Complexity/file_name/@filename"/></td>
						</tr>
						<tr>
							<td>Language Scope</td>
							<td>
								<xsl:value-of select="Language_Scope/max_value"/> [<xsl:value-of select="Language_Scope/file_name/func_name"/>]
							</td>
							<td><xsl:value-of select="Language_Scope/file_name/@filename"/></td>
						</tr>
						<tr class="open-details-btn">
							<td>Goto Statements
								<button class="details-btn">+</button>
							</td>
							<td><xsl:value-of select="Goto_Statements/max_value"/></td>
							<td></td>		
						</tr>
						<tr class="content">
							<td colspan="3">
								<table class="report_main" style="table-layout:fixed">
									<tr>
										<th>Function(s)</th>
										<th>File Path</th>
									</tr>
									
									<xsl:for-each select="Goto_Statements/file_name">
										<tr>
											<td>
												<xsl:value-of select="func_name"/>
											</td>
											<td><xsl:value-of select="@filename"/></td>
										</tr>
									</xsl:for-each>
								</table>
							</td>
						</tr>
						<tr class="open-details-btn">
							<td>Return Statements
								<button class="details-btn">+</button>
							</td>
							<td><xsl:value-of select="Return_Statements/max_value"/></td>
							<td></td>
						</tr>
						<tr class="content">
							<td colspan="3">
								<table class="report_main" style="table-layout:fixed">
									<tr>
										<th>Function(s)</th>
										<th>File Path</th>
									</tr>
									<xsl:for-each select="Return_Statements/file_name">
										<tr>
											<td>
												<xsl:value-of select="func_name"/>
											</td>
											<td><xsl:value-of select="@filename"/></td>
										</tr>
									</xsl:for-each>
								</table>
							</td>
						</tr>
					</table>
            </body>
			<script><![CDATA[
				(function() {
					const openDetailButtons = document.querySelectorAll(".open-details-btn")
					if(!openDetailButtons.length) {
						return;
					}
					openDetailButtons.forEach((openDetailBtn) => {
						openDetailBtn.addEventListener('click', function(e) {
							if(e.target && e.target.nodeName === "BUTTON"){
								const contentElm = this.nextSibling.nextSibling
								if(contentElm.classList.contains("content")){
									if(contentElm.style.display === "table-row"){
										contentElm.style.display = "none"
										e.toElement.innerText = "+"
									} else {
										contentElm.style.display = "table-row"
										e.toElement.innerText = "-"
									}
								}
							}
						})				
					})
				})();
			]]></script>
        </html>
    </xsl:template>
</xsl:stylesheet>