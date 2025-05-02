# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s medialog.hilversum -t test_aanbieder.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src medialog.hilversum.testing.MEDIALOG_HILVERSUM_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/medialog/hilversum/tests/robot/test_aanbieder.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Aanbieder
  Given a logged-in site administrator
    and an add Aanbieder form
   When I type 'My Aanbieder' into the title field
    and I submit the form
   Then a Aanbieder with the title 'My Aanbieder' has been created

Scenario: As a site administrator I can view a Aanbieder
  Given a logged-in site administrator
    and a Aanbieder 'My Aanbieder'
   When I go to the Aanbieder view
   Then I can see the Aanbieder title 'My Aanbieder'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Aanbieder form
  Go To  ${PLONE_URL}/++add++Aanbieder

a Aanbieder 'My Aanbieder'
  Create content  type=Aanbieder  id=my-aanbieder  title=My Aanbieder

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Aanbieder view
  Go To  ${PLONE_URL}/my-aanbieder
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Aanbieder with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Aanbieder title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
