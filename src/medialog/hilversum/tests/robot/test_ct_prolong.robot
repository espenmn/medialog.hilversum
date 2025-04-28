# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s medialog.hilversum -t test_prolong.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src medialog.hilversum.testing.MEDIALOG_HILVERSUM_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/medialog/hilversum/tests/robot/test_prolong.robot
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

Scenario: As a site administrator I can add a Prolong
  Given a logged-in site administrator
    and an add Prolong form
   When I type 'My Prolong' into the title field
    and I submit the form
   Then a Prolong with the title 'My Prolong' has been created

Scenario: As a site administrator I can view a Prolong
  Given a logged-in site administrator
    and a Prolong 'My Prolong'
   When I go to the Prolong view
   Then I can see the Prolong title 'My Prolong'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Prolong form
  Go To  ${PLONE_URL}/++add++Prolong

a Prolong 'My Prolong'
  Create content  type=Prolong  id=my-prolong  title=My Prolong

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Prolong view
  Go To  ${PLONE_URL}/my-prolong
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Prolong with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Prolong title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
